# Seed42 GPU Queue Commands

Use this only after approving the GPU stage. It assumes the cloud repo has
already pulled the commit containing `.agent/cross_dataset_validation/seed42_gpu_queue.sh`.

## Start Detached Queue

```bash
cd /root/llamarec
git fetch origin main
git checkout main
git pull --ff-only origin main
chmod +x .agent/cross_dataset_validation/seed42_gpu_queue.sh
LOG="outputs/cross_dataset_validation/amazon-musical-instruments/seed42_gpu_queue_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$(dirname "$LOG")"
nohup bash .agent/cross_dataset_validation/seed42_gpu_queue.sh > "$LOG" 2>&1 < /dev/null &
echo "PID=$!"
echo "LOG=$LOG"
```

## Check Progress

```bash
cd /root/llamarec
STATUS="outputs/cross_dataset_validation/amazon-musical-instruments/seed42_queue_status.txt"
LOG="$(ls -t outputs/cross_dataset_validation/amazon-musical-instruments/seed42_gpu_queue_*.log | head -1)"
echo "STATUS=$STATUS"
cat "$STATUS" 2>/dev/null || true
echo "LOG=$LOG"
tail -n 80 "$LOG"
ps aux | grep -E "seed42_gpu_queue|train_y|train_n|train_m|evaluate_|base_zero_shot|sasrec" | grep -v grep || true
nvidia-smi || true
```

## Stop Queue If Needed

```bash
cd /root/llamarec
pkill -f ".agent/cross_dataset_validation/seed42_gpu_queue.sh" || true
pkill -f "src.train.train_y" || true
pkill -f "src.train.train_n" || true
pkill -f "src.train.train_m" || true
pkill -f "src.inference.base_zero_shot" || true
pkill -f "src.inference.evaluate_y_adapter" || true
pkill -f "src.inference.evaluate_n_adapter" || true
pkill -f "src.inference.evaluate_m_adapter" || true
pkill -f "src.baselines.sasrec" || true
ps aux | grep -E "seed42_gpu_queue|train_y|train_n|train_m|evaluate_|base_zero_shot|sasrec" | grep -v grep || true
```
