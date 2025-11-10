Windows UTC Time Fix for Dual Boot

This .reg file fixes incorrect time issues when dual-booting Windows and Linux/macOS.

By default, Windows treats the hardware clock as local time, while Linux/macOS use UTC.
This mismatch causes the clock to shift a few hours after switching systems. 
The patch makes Windows read the hardware clock as UTC, keeping both systems in sync.
