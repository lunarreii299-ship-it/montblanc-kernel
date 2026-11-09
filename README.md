# montblanc-kernel
Samsung SM-W2014 (Montblanc) kernel work on top of LineageOS `android_kernel_samsung_msm8974` (3.4.113).

Stage 1: new kernel + **stock** 4.3 ramdisk + **stock** dt.img, to validate display (both screens), touch,
keypad, Wi-Fi, Bluetooth and audio before moving to Android 11 userspace.
Recovery from a bad test: re-flash the stock boot.img from your firmware in Odin (AP slot).
