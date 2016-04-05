#bin/bash           
echo traditional dataset audio files slicing...
for file in ~/Tesis/traditional_dataset/allemande/fragments/*_mono.wav
do
echo $file
python slicing.py $file
done
for file in ~/Tesis/traditional_dataset/syrinx/fragments/*_mono.wav
do
echo $file
python slicing.py $file
done
     
