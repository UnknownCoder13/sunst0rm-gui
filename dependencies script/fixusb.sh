echo "This fixes USB issues on Linux by restarting USBMUXD" 
sudo systemctl stop usbmuxd && sudo usbmuxd -p -f
echo "Done! Please keep this terminal Minimized!"