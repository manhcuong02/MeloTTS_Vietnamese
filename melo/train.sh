CONFIG=/storage2/melotts/dataset/infore/config.json
DUMMY=/storage2/melotts/dataset
GPUS=1
G=/storage2/melotts/melo/logs/infore/G_4000.pth
D=/storage2/melotts/melo/logs/infore/D_4000.pth
DUR=/storage2/melotts/melo/logs/infore/DUR_4000.pth
MODEL_NAME=$(basename "$(dirname $CONFIG)")

PORT=10902

rm -r DUMMY
ln -s $DUMMY DUMMY

# while : # auto-resume: the code sometimes crash due to bug of gloo on some gpus
# do
CUDA_VISIBLE_DEVICES=0 torchrun --nproc_per_node=$GPUS \
        --master_port=$PORT \
    train.py --c $CONFIG --model $MODEL_NAME
    --pretrain_G $G --pretrain_D $D --pretrain_dur $DUR

# for PID in $(ps -aux | grep $CONFIG | grep python | awk '{print $2}')
# do
#     echo $PID
#     kill -9 $PID
# done
# sleep 30
# done
