//! rci_scan — streaming census for an ecdsa.fail op stream.
//!
//! The circuit is ~1.23e9 ops / ~69 GB decompressed. Python cannot hold that,
//! so the scan lives here: pipe the decompressed stream in and get JSON out.
//!
//!   zstd -d -c ops.bin | rci_scan [--lanes 255,256,257,258] [--stride N]
//!
//! Record layout (56 bytes, little-endian, from src/bin/eval_circuit.rs):
//!   u32 kind | u32 pad | u64 q_control2 | u64 q_control1 | u64 q_target
//!   u64 c_target | u64 c_condition | u64 r_target
//!
//! Build:  rustc -O -o rci_scan rci_scan.rs

use std::io::{self, Read};

const REC: usize = 56;
const NIL: u64 = u64::MAX;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut watch: Vec<u64> = Vec::new();
    let mut stride: u64 = 1;
    let mut hist_kinds: Vec<usize> = Vec::new();
    let mut buckets: u64 = 20;
    let mut total_hint: u64 = 0;
    let mut expect_q: u64 = 0;
    let mut max_ops: u64 = u64::MAX;
    let mut lifetime = false;
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--lanes" => {
                i += 1;
                if i < args.len() {
                    for t in args[i].split(',') {
                        if let Ok(v) = t.trim().parse::<u64>() {
                            watch.push(v);
                        }
                    }
                }
            }
            "--stride" => {
                i += 1;
                if i < args.len() {
                    stride = args[i].parse().unwrap_or(1).max(1);
                }
            }
            "--hist-kind" => {
                i += 1;
                if i < args.len() {
                    for t in args[i].split(',') {
                        if let Ok(v) = t.trim().parse::<usize>() {
                            hist_kinds.push(v);
                        }
                    }
                }
            }
            "--buckets" => {
                i += 1;
                if i < args.len() {
                    buckets = args[i].parse().unwrap_or(20).max(1);
                }
            }
            "--total" => {
                i += 1;
                if i < args.len() {
                    total_hint = args[i].parse().unwrap_or(0);
                }
            }
            "--expect-q" => {
                i += 1;
                if i < args.len() {
                    expect_q = args[i].parse().unwrap_or(0);
                }
            }
            "--max-ops" => {
                i += 1;
                if i < args.len() {
                    max_ops = args[i].parse().unwrap_or(u64::MAX);
                }
            }
            "--lifetime" => {
                lifetime = true;
            }
            _ => {}
        }
        i += 1;
    }
    let (wmin, wmax) = if watch.is_empty() {
        (u64::MAX, 0u64)
    } else {
        (
            *watch.iter().min().unwrap(),
            *watch.iter().max().unwrap(),
        )
    };

    let stdin = io::stdin();
    let mut r = io::BufReader::with_capacity(1 << 23, stdin.lock());
    let mut buf = vec![0u8; 1 << 23];
    let mut carry = 0usize;

    let mut counts = [0u64; 32];
    let mut toffoli: u64 = 0;
    let mut peak: u64 = 0;
    let mut n: u64 = 0;
    let mut max_t: u64 = 0;
    let mut holes: Vec<(u64, u64, u32)> = Vec::new();
    let mut hole_seen = vec![false; watch.len()];
    let mut hist: Vec<Vec<u64>> = vec![vec![0u64; buckets as usize]; hist_kinds.len()];
    // First/last use per qubit id bounds each lane's live interval. Sweeping those
    // intervals gives the occupancy curve, i.e. WHERE in the stream the peak sits.
    const QCAP: usize = 8192;
    let mut first = vec![u64::MAX; QCAP];
    let mut last = vec![0u64; QCAP];

    loop {
        let got = r.read(&mut buf[carry..]).unwrap_or(0);
        if got == 0 {
            break;
        }
        let total = carry + got;
        let nrec = total / REC;
        for k in 0..nrec {
            // stride: still count, only spend parse effort where asked
            n += 1;
            if stride > 1 && (n % stride) != 0 {
                continue;
            }
            let o = k * REC;
            let kind = u32::from_le_bytes(buf[o..o + 4].try_into().unwrap());
            if !hist_kinds.is_empty() && total_hint > 0 {
                if let Some(hi) = hist_kinds.iter().position(|&h| h == kind as usize) {
                    let b = (((n - 1) * buckets) / total_hint).min(buckets - 1) as usize;
                    hist[hi][b] += 1;
                }
            }
            let c2 = u64::from_le_bytes(buf[o + 8..o + 16].try_into().unwrap());
            let c1 = u64::from_le_bytes(buf[o + 16..o + 24].try_into().unwrap());
            let tgt = u64::from_le_bytes(buf[o + 24..o + 32].try_into().unwrap());
            if (kind as usize) < 32 {
                counts[kind as usize] += 1;
            }
            if kind == 13 || kind == 14 {
                toffoli += 1;
            }
            if kind == 11 {
                max_t = max_t.max(tgt);
            }
            for q in [c2, c1, tgt] {
                if q != NIL && q > peak {
                    peak = q;
                }
                if lifetime && q != NIL && (q as usize) < QCAP {
                    let qi = q as usize;
                    let idx = n - 1;
                    if idx < first[qi] {
                        first[qi] = idx;
                    }
                    if idx > last[qi] {
                        last[qi] = idx;
                    }
                }
                if !watch.is_empty() && q >= wmin && q <= wmax {
                    for (wi, &w) in watch.iter().enumerate() {
                        if q == w && !hole_seen[wi] {
                            hole_seen[wi] = true;
                            holes.push((n - 1, w, kind));
                        }
                    }
                }
            }
        }
        let rem = total - nrec * REC;
        if rem > 0 {
            buf.copy_within(nrec * REC..total, 0);
        }
        carry = rem;
        if got == 0 {
            break;
        }
    }

    let _ = max_t;
    let kinds: Vec<String> = (0..18)
        .filter(|&k| counts[k] > 0)
        .map(|k| format!("\"{}\":{}", kind_name(k), counts[k]))
        .collect();
    let hole_json: Vec<String> = holes
        .iter()
        .map(|(idx, lane, kind)| {
            format!(
                "{{\"op_index\":{},\"lane\":{},\"kind\":\"{}\"}}",
                idx,
                lane,
                kind_name(*kind as usize)
            )
        })
        .collect();
    // ---- occupancy curve -------------------------------------------------
    let mut occ_json = String::from("null");
    if lifetime {
        let mut ev: Vec<(u64, i32)> = Vec::new();
        for q in 0..QCAP {
            if first[q] != u64::MAX {
                ev.push((first[q], 1));
                ev.push((last[q] + 1, -1));
            }
        }
        ev.sort_unstable();
        let tot = if total_hint > 0 { total_hint } else { n.max(1) };
        let mut buck = vec![0u64; buckets as usize];
        let mut cur: i64 = 0;
        let mut peak_live: u64 = 0;
        let mut peak_live_start: u64 = 0;
        let mut ei = 0usize;
        let mut prev: u64 = 0;
        while ei < ev.len() {
            let idx = ev[ei].0;
            if cur > 0 && idx > prev {
                let b0 = (prev * buckets / tot).min(buckets - 1) as usize;
                let b1 = ((idx - 1) * buckets / tot).min(buckets - 1) as usize;
                for b in b0..=b1 {
                    if (cur as u64) > buck[b] {
                        buck[b] = cur as u64;
                    }
                }
            }
            while ei < ev.len() && ev[ei].0 == idx {
                cur += ev[ei].1 as i64;
                ei += 1;
            }
            if cur > 0 && cur as u64 > peak_live {
                peak_live = cur as u64;
                peak_live_start = idx;
            }
            prev = idx;
        }
        let row: Vec<String> = buck.iter().map(|c| c.to_string()).collect();
        occ_json = format!(
            "{{\"peak_concurrent_lanes\":{},\"peak_starts_at_op\":{},\"occupancy_by_bucket\":[{}]}}",
            peak_live,
            peak_live_start,
            row.join(",")
        );
    }

    // ---- pre-submit certificate -----------------------------------------
    // Only claims what a static scan can actually prove: the Q axis and the
    // MAX_OPS cap are exact; T is NOT (the scored axis is executed Toffoli).
    let q_got = if peak == u64::MAX { 0 } else { peak + 1 };
    let mut checks: Vec<String> = Vec::new();
    let mut all_ok = true;
    if expect_q > 0 {
        let ok = q_got == expect_q;
        all_ok &= ok;
        checks.push(format!(
            "{{\"check\":\"peak_qubits\",\"got\":{},\"want\":{},\"ok\":{}}}",
            q_got, expect_q, ok
        ));
    }
    let ops_ok = n <= max_ops;
    all_ok &= ops_ok;
    checks.push(format!(
        "{{\"check\":\"ops_under_cap\",\"got\":{},\"cap\":{},\"ok\":{}}}",
        n, max_ops, ops_ok
    ));
    if !watch.is_empty() {
        all_ok &= holes.is_empty();
        checks.push(format!(
            "{{\"check\":\"no_omitted_rail_touch\",\"touches\":{},\"ok\":{}}}",
            holes.len(),
            holes.is_empty()
        ));
    }

    let hist_json: Vec<String> = hist_kinds
        .iter()
        .enumerate()
        .map(|(hi, &k)| {
            let row: Vec<String> = hist[hi].iter().map(|c| c.to_string()).collect();
            format!("\"{}\":[{}]", kind_name(k), row.join(","))
        })
        .collect();
    println!(
        "{{\n  \"ops\": {},\n  \"sampled_stride\": {},\n  \"toffoli\": {},\n  \"peak_qubit_id\": {},\n  \"qubits_upper_bound\": {},\n  \"toffoli_fraction\": {:.6},\n  \"kinds\": {{{}}},\n  \"watch_lanes\": {:?},\n  \"holes_clean\": {},\n  \"hole_first_touch\": [{}],\n  \"position_histogram_buckets\": {},\n  \"position_histogram\": {{{}}},\n  \"occupancy\": {}\n}}",
        n,
        stride,
        toffoli,
        if peak == u64::MAX { -1i64 } else { peak as i64 },
        if peak == u64::MAX { 0u64 } else { peak + 1 },
        if n > 0 { toffoli as f64 / n as f64 } else { 0.0 },
        kinds.join(","),
        watch,
        holes.is_empty(),
        hole_json.join(","),
        buckets,
        hist_json.join(","),
        occ_json
    );
    eprintln!(
        "{{\"certificate\":{{\"ok\":{},\"checks\":[{}],\"note\":\"emitted CCX = {} is NOT the scored toffoli; the scored axis is executed Toffoli averaged over shots. Q and the ops cap are exact here.\"}}}}",
        all_ok,
        checks.join(","),
        toffoli
    );
    if !all_ok {
        std::process::exit(1);
    }
}

fn kind_name(k: usize) -> &'static str {
    match k {
        0 => "Neg",
        1 => "Register",
        2 => "AppendToRegister",
        3 => "BitInvert",
        4 => "BitStore0",
        5 => "BitStore1",
        6 => "X",
        7 => "Z",
        8 => "CX",
        9 => "CZ",
        10 => "Swap",
        11 => "R",
        12 => "Hmr",
        13 => "CCX",
        14 => "CCZ",
        15 => "PushCondition",
        16 => "PopCondition",
        17 => "DebugPrint",
        _ => "Unknown",
    }
}
