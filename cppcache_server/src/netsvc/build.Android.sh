echo "**** build netsvc ****"
(cd jni/ && ndk-build clean && ndk-build)

echo "**** copy include ****"
mkdir ../../../../include/netsvc/ -p
cp -rfT include/ ../../../../include/netsvc/0.1.4/

echo "**** move libs ****"
mkdir ../../../../lib/netsvc/0.1.4/Android -p 
mv obj/local/armeabi/libnetsvc.a ../../../../lib/netsvc/0.1.4/Android/
rm obj -rf

