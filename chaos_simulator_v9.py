import random
import math
import time

def get_primes(n):
    primes = []
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return primes

class ProfiledChaosGovernor:
    def __init__(self, profile="smooth"):
        self.all_primes = get_primes(10000)
        self.risk_level = 0.05
        self.latency_baseline = 1.5
        self.window_size = 15
        self.profile = profile # "smooth" or "contrast"

    def observe_and_update(self, actual_latency):
        if actual_latency > self.latency_baseline * 2.5:
            self.risk_level = min(0.99, (self.risk_level * 1.5) + 0.1)
        else:
            self.risk_level = max(0.01, self.risk_level * 0.85)
        return self.risk_level

    def get_next_delay(self):
        if self.profile == "contrast":
            # 短线高反差模式：禁用 Y 和 C
            if self.risk_level < 0.3:
                start_idx = random.randint(0, 40) # Hyper 模式
                mode = "H"
            else:
                # 风险一旦抬头，直接切入 Chaos，跳过中间地带
                start_idx = random.randint(300, len(self.all_primes) - self.window_size - 1)
                mode = "X"
        else:
            # 长线平滑模式
            if self.risk_level < 0.15:
                start_idx = random.randint(0, 25); mode = "H"
            elif self.risk_level < 0.35:
                start_idx = random.randint(25, 60); mode = "Y"
            elif self.risk_level < 0.7:
                start_idx = random.randint(80, 280); mode = "C"
            else:
                start_idx = random.randint(300, len(self.all_primes) - self.window_size - 1); mode = "X"

        pool = self.all_primes[start_idx : start_idx + self.window_size]
        base_prime = random.choice(pool)
        u = random.random()
        delay = -math.log(u) * base_prime
        return delay, mode

def run_profile_test(profile_name, duration_hours=4):
    gov = ProfiledChaosGovernor(profile=profile_name)
    current_time = 0
    duration_secs = duration_hours * 3600
    stats = []
    
    slots_count = duration_hours * 60
    risk_snapshot = [0.0] * slots_count
    mode_snapshot = [" "] * slots_count

    while current_time < duration_secs:
        hour = current_time / 3600
        slot_idx = int(current_time // 60)
        
        # 模拟环境：2-3h 期间风险波动
        if 2 <= hour <= 3.5:
            simulated_latency = random.uniform(5.0, 10.0)
        else:
            simulated_latency = random.uniform(1.2, 1.8)

        risk = gov.observe_and_update(simulated_latency)
        delay, mode = gov.get_next_delay()
        
        if slot_idx < slots_count:
            stats.append({'slot': slot_idx, 'risk': risk, 'mode': mode})
            
        end_slot = min(slots_count, int((current_time + delay) // 60))
        for i in range(slot_idx, end_slot):
            risk_snapshot[i] = risk
            mode_snapshot[i] = mode
            
        current_time += delay
    
    return stats, risk_snapshot, mode_snapshot

def visualize_comparison():
    hours = 4
    slots = hours * 60
    
    print(f"📊 Chaos Profiles 对比仿真 (时长: {hours}h)")
    print("   [ H=Hyper, Y=Yield, C=Cruise, X=Chaos ]")
    print("-" * (slots + 20))

    # 测试 Smooth
    stats_s, risk_s, mode_s = run_profile_test("smooth", hours)
    # 测试 Contrast
    stats_c, risk_c, mode_c = run_profile_test("contrast", hours)

    # 打印对比
    print(f"模式 A (Smooth - 长线) | {''.join(mode_s)}")
    print(f"模式 B (Contrast - 短线)| {''.join(mode_c)}")
    print("-" * (slots + 20))
    
    # 风险线（共享环境，所以只打一个展示）
    risk_line = "环境风险趋势       |"
    for r in risk_s:
        risk_line += "🔥" if r > 0.7 else ("🌊" if r > 0.3 else "░")
    print(risk_line)
    print("-" * (slots + 20))

    print(f"📈 总结:")
    print(f"   [Smooth]   完成: {len(stats_s)} 任务 | 时速: {len(stats_s)/hours:.2f} j/h")
    print(f"   [Contrast] 完成: {len(stats_c)} 任务 | 时速: {len(stats_c)/hours:.2f} j/h")

if __name__ == "__main__":
    visualize_comparison()
