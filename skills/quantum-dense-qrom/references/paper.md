# Source and transfer

[Dense encoding QROM v1](https://arxiv.org/html/2610.02321v1), section II and Appendix A.
The construction stores paired classical table bits through X/Z Pauli choices on dirty qubits, reads via phase kickback and restores the borrowed state with the true inverse load. Packetization can improve the leading loading term. Those asymptotic factors are not whole-circuit savings: row reads, finite table shape and available dirty workspace matter.

Application hypothesis: replacing a measured lookup bottleneck may alter its resource curve. Verify the complete gate-set compatibility before integration.
