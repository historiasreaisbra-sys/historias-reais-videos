#!/bin/bash
# uso: finish_day.sh N narr.wav bed.wav "TITULO com *PALAVRA*" PALAVRA "condição" "teaser" slug hookimg
set -e
N=$1; NARR=$2; BED=$3; TITLE=$4; WORD=$5; COND=$6; TEASER=$7; SLUG=$8; HOOK=$9
K=/home/claude/v1; D=$K/d$N; NN=$(printf %02d $N)
cd $D
TOT=$(cd $K/scripts && python3 render_day.py cfg$N total)
ffmpeg -y -v error -i $NARR -af "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000" /tmp/n$N.wav
ffmpeg -y -v error -i /tmp/n$N.wav -i $BED -filter_complex "[1:a]aresample=48000,volume=0.12[b];[0:a][b]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95,atrim=0:$TOT[a]" -map "[a]" -c:a pcm_s16le mix.wav
printf "file 'build/c0.mp4'\nfile 'build/c1.mp4'\n" > list.txt
ffmpeg -y -v error -f concat -safe 0 -i list.txt -i mix.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 27 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest base.mp4
ffmpeg -y -v error -i base.mp4 -i $K/perfilD/marca_dagua.png -filter_complex "overlay=W-w-36:60" -c:v libx264 -preset veryfast -crf 27 -pix_fmt yuv420p -c:a copy marca.mp4
python3 -c "
import sys; sys.path.insert(0,'$K/scripts')
from crescimento import endcard, title_overlay, cover
title_overlay('''$TITLE''','titulo.png')
cover('img/$HOOK.jpg','''$TITLE''','capa-dia-$NN.jpg',dia=$N)
endcard('marca.mp4','''$WORD''','''$COND''','''$TEASER''','cartao.png')"
bash $K/scripts/finalizar.sh marca.mp4 titulo.png cartao.png historias-reais-$NN-$SLUG.mp4
F=historias-reais-$NN-$SLUG.mp4; L=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F)
rm -f chk_*.jpg
for t in 0.5 2.5 20 $(python3 -c "print(round($L-4.6,2))") $(python3 -c "print(round($L-1,2))"); do ffmpeg -y -v error -ss $t -i $F -frames:v 1 -vf scale=360:640 chk_$t.jpg; done
python3 -c "
from PIL import Image; import glob
fs=sorted(glob.glob('chk_*.jpg'),key=lambda f:float(f[4:-4])); s=Image.new('RGB',(360*len(fs)+360,640))
for i,f in enumerate(fs): s.paste(Image.open(f),(i*360,0))
s.paste(Image.open('capa-dia-$NN.jpg').resize((360,640)),(len(fs)*360,0))
s.save('chk.jpg')"
