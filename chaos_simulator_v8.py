import random
import math
import time

def get_primes(n):
    """获取 n 以内的所有质数"""
    primes = []
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return primes

class TieredChaosGovernor:
    def __init__(self):
        self.all_primes = get_primes(10000) # 1229个质数
        self.risk_level = 0.05
        self.latency_baseline = 1.5
        self.window_size = 15

    def observe_and_update(self, actual_latency):
        # 贝叶斯更新逻辑
        if actual_latency > self.latency_baseline * 2.5:
            self.risk_level = min(0.99, (self.risk_level * 1.5) + 0.1)
        else:
            self.risk_level = max(0.01, self.risk_level * 0.85)
        return self.risk_level

    def get_next_delay(self):
        # 重新锚定索引以匹配时速目标
        # Tier 0 (Hyper-Yield): [2, 150] -> ~24 j/h
        # Tier 1 (Target-Yield): [150, 400] -> ~18 j/h
        # Tier 2 (Safe): [400, 2000] -> ~6 j/h
        # Tier 3 (Chaos): [2000, 10000] -> < 1 j/h
        
        if self.risk_level < 0.15:
            start_idx = random.randint(0, 25) 
            mode = "H" # Hyper
        elif self.risk_level < 0.35:
            start_idx = random.randint(25, 60)
            mode = "Y" # Yield (Target)
        elif self.risk_level < 0.7:
            start_idx = random.randint(80, 280)
            mode = "C" # Cruise
        else:
            start_idx = random.randint(300, len(self.all_primes) - self.window_size - 1)
            mode = "X" # Chaos

        pool = self.all_primes[start_idx : start_idx + self.window_size]
        base_prime = random.choice(pool)
        
        u = random.random()
        delay = -math.log(u) * base_prime
        return delay, mode

def run_simulation_v8(duration_hours=8):
    gov = TieredChaosGovernor()
    current_time = 0
    duration_secs = duration_hours * 3600
    stats = []

    print(f"🌡️ 10,000质数域 Tiered 仿真 v8.1 启动...")
    print(f"   目标: 18 j/h (主战区) | 极限: 10,000s 隐身 | 质数总量: {len(gov.all_primes)}")
    print("-" * 80)

    # 预生成一分钟一个的风险快照
    slots_count = duration_hours * 60
    risk_snapshot = [0.0] * slots_count
    mode_snapshot = [" "] * slots_count
    
    # 仿真主循环
    while current_time < duration_secs:
        hour = current_time / 3600
        slot_idx = int(current_time // 60)
        
        # 模拟环境：3-5h 风险期
        if 3 <= hour <= 5.5:
            simulated_latency = random.uniform(5.0, 10.0)
        else:
            simulated_latency = random.uniform(1.2, 1.8)

        risk = gov.observe_and_update(simulated_latency)
        delay, mode = gov.get_next_delay()
        
        # 记录每个任务
        if slot_idx < slots_count:
            stats.append({'slot': slot_idx, 'risk': risk, 'mode': mode})
            
        # 填充快照（直到下一个任务发生前，系统都处于该风险和模式下）
        end_slot = min(slots_count, int((current_time + delay) // 60))
        for i in range(slot_idx, end_slot):
            risk_snapshot[i] = risk
            mode_snapshot[i] = mode
            
        current_time += delay

    # --- 可视化 ---
    density_map = [0] * slots_count
    for s in stats:
        density_map[s['slot']] += 1

    print(f"\n📊 战术呼吸感看板 (每列1分钟)")
    print("   [ █=任务 | H=Hyper, Y=Yield, C=Cruise, X=Chaos ]")
    
    for h in range(3, 0, -1):
        line = f"密度 {h:d} |"
        for i in range(slots_count):
            line += "█" if density_map[i] >= h else " "
        print(line)

    # 风险与模式
    risk_line = "风险线 |"
    mode_line = "模式区 |"
    for i in range(slots_count):
        r = risk_snapshot[i]
        risk_line += "🔥" if r > 0.7 else ("🌊" if r > 0.35 else "░")
        mode_line += mode_snapshot[i]
    
    print(risk_line)
    print(mode_line)
    print("-" * (slots_count + 15))
    print(f"📈 总结: {duration_hours}h完成 {len(stats)} 任务 | 平均时速 {len(stats)/duration_hours:.2f} j/h")

if __name__ == "__main__":
    run_simulation_v8()
