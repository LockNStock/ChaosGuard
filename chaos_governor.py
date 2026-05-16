import random
import math
import time

class ChaosGovernor:
    """
    v7.0 行业级混沌调度器
    集成功能：
    1. 动态滑动窗口 (1000质数域)
    2. 泊松采样 (微观平滑)
    3. 浮动概率 (基于质数偏移)
    4. 贝叶斯反馈循环 (基于响应延迟的风险感知)
    """
    def __init__(self, baseline_latency=1.5):
        self.primes = self._get_primes(1000)
        self.risk_level = 0.05  # 先验风险 5%
        self.latency_baseline = baseline_latency # 正常响应基准
        self.last_delay = 0
        
    def _get_primes(self, n):
        res = []
        for num in range(2, n + 1):
            for i in range(2, int(num**0.5) + 1):
                if (num % i) == 0: break
            else: res.append(num)
        return res

    def observe_and_update(self, actual_latency):
        """
        贝叶斯反馈：根据观测到的服务器响应延迟更新风险等级
        """
        # 风险因子：如果延迟高于基准，则增加风险；否则降低
        if actual_latency > self.latency_baseline * 2.5:
            # 延迟严重，风险快速积累
            self.risk_level = (self.risk_level * 1.5) + 0.1
        elif actual_latency > self.latency_baseline:
            # 稍微拥堵，风险缓慢提升
            self.risk_level = (self.risk_level * 1.1) + 0.02
        else:
            # 响应极快，信心增强，风险衰减
            self.risk_level *= 0.85
            
        # 归一化处理
        self.risk_level = min(max(self.risk_level, 0.01), 0.99)
        return self.risk_level

    def get_next_delay(self):
        """
        基于当前风险等级生成混沌延迟
        """
        # 核心逻辑：风险越高，滑动窗口的最小值越高 (被迫减速)
        # 风险 1% -> 起点 15s | 风险 99% -> 起点 500s+
        dynamic_min = 15 + (self.risk_level * 550)
        
        # 1. 动态生成大窗口子池
        macro_pool = self._get_sliding_pool(dynamic_min, 1000)
        
        # 2. 浮动概率决策
        chaos_seed = random.choice(macro_pool)
        # 概率受质数偏移影响，并受当前风险等级直接压制
        burst_prob = ((chaos_seed - 100) % 100) / 100.0
        burst_prob *= (1.0 - self.risk_level)

        if random.random() < burst_prob:
            # 模式 A: 爆发/短脉冲
            # 使用局部小窗口
            micro_pool = self._get_sliding_pool(dynamic_min, dynamic_min + 150)
            base = random.choice(micro_pool)
        else:
            # 模式 B: 巡航/深呼吸
            base = random.choice(macro_pool)

        # 3. 泊松抖动采样 (指数分布转换)
        delay = -math.log(random.random() or 1e-7) * base
        self.last_delay = delay
        return delay

    def _get_sliding_pool(self, min_val, max_val, min_len=5, max_len=20):
        """滑动窗口池生成"""
        candidates = [i for i, p in enumerate(self.primes) if min_val <= p <= max_val]
        if not candidates: return [int(min_val)]
        
        target_len = random.randint(min_len, max_len)
        start_idx = random.choice(candidates)
        
        # 边界保护 (Back-shifting)
        if start_idx + target_len > len(self.primes):
            start_idx = max(0, len(self.primes) - target_len)
            
        return self.primes[start_idx : start_idx + target_len]

if __name__ == "__main__":
    # 模块自测逻辑
    gov = ChaosGovernor()
    print("🧪 ChaosGovernor 模块自测中...")
    for i in range(5):
        d = gov.get_next_delay()
        print(f"Round {i+1}: Delay={d:.2f}s | Risk={gov.risk_level:.1%}")
        # 模拟不同的反馈
        gov.observe_and_update(random.uniform(0.5, 5.0))
