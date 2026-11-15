//! qcount: independent distinct-qubit-id count of an ops.bin (does not use the evaluator's loader or nq logic).
//! Prints one line: ops=N distinct_q=D max_id=M dense=true|false
use std::io::{BufReader, Read};
fn main() {
    let path = std::env::args().nth(1).expect("usage: qcount ops.bin");
    let mut f = std::fs::File::open(&path).expect("open");
    let mut h = [0u8; 16];
    f.read_exact(&mut h).expect("header");
    assert_eq!(&h[..8], b"QECCOPSZ", "bad magic");
    let n = u64::from_le_bytes(h[8..].try_into().unwrap()) as usize;
    let mut dec = zstd::stream::read::Decoder::new(BufReader::with_capacity(1 << 20, f)).expect("zstd");
    dec.window_log_max(27).expect("wl");
    let mut seen = vec![false; 1 << 22];
    let mut big = std::collections::HashSet::new();
    let (mut distinct, mut maxid) = (0u64, 0u64);
    let mut buf = vec![0u8; (1 << 16) * 56];
    let mut left = n;
    while left > 0 {
        let m = left.min(1 << 16);
        dec.read_exact(&mut buf[..m * 56]).expect("short read");
        for r in buf[..m * 56].chunks_exact(56) {
            for off in [8usize, 16, 24] {
                let q = u64::from_le_bytes(r[off..off + 8].try_into().unwrap());
                if q == u64::MAX { continue; }
                maxid = maxid.max(q);
                let new = if (q as usize) < seen.len() { let s = &mut seen[q as usize]; let nw = !*s; *s = true; nw } else { big.insert(q) };
                if new { distinct += 1; }
            }
        }
        left -= m;
    }
    println!("ops={} distinct_q={} max_id={} dense={}", n, distinct, maxid, distinct == maxid + 1);
}
