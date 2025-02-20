CONFIG=/home/misa/home/misa/MeloTTS_Vietnamese/dataset/NHLy/config.json
DUMMY=/home/misa/home/misa/MeloTTS_Vietnamese/dataset
GPUS=1
# # pretrained models from MISA team
G=/home/misa/home/misa/MeloTTS_Vietnamese/melo/logs/NHLy/G_7000.pth
D=/home/misa/home/misa/MeloTTS_Vietnamese/melo/logs/NHLy/D_7000.pth
DUR=/home/misa/home/misa/MeloTTS_Vietnamese/melo/logs/NHLy/DUR_7000.pth
# pretrained models from author
# G=/home/misa/home/misa/MeloTTS_Vietnamese/ckpts/G.pth
# D=/home/misa/home/misa/MeloTTS_Vietnamese/ckpts/D.pth
# DUR=/home/misa/home/misa/MeloTTS_Vietnamese/ckpts/DUR.pth
MODEL_NAME=$(basename "$(dirname $CONFIG)")

PORT=10902

rm -r DUMMY
ln -s $DUMMY DUMMY

# while : # auto-resume: the code sometimes crash due to bug of gloo on some gpus
# do
CUDA_VISIBLE_DEVICES=0 torchrun --nproc_per_node=$GPUS \
        --master_port=$PORT \
    train.py --c $CONFIG --model $MODEL_NAME \
    --pretrain_G $G --pretrain_D $D --pretrain_dur $DUR

# for PID in $(ps -aux | grep $CONFIG | grep python | awk '{print $2}')
# do
#     echo $PID
#     kill -9 $PID
# done
# sleep 30
# done