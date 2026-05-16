#!/usr/bin/env python3
import random
import math
from chaos_governor import ChaosGovernor

def simulate_v7_bayesian(duration_hours=8):
    gov = ChaosGovernor(baseline_latency=1.5)
    duration_secs = duration_hours * 3600
    current_time = 0
    total_jobs = 0
    
    # 记录数据：(时间, 任务数, 风险等级)
    stats = [] # 每5分钟一个数据点
    
    print(f"🌡️ 贝叶斯自适应仿真 v7.0 启动...")
    print(f"   模拟场景: 0-3h 正常 | 3-5h 环境恶化(风控) | 5-8h 逐渐恢复")
    print("-" * 70)

    while current_time < duration_secs:
        # --- 模拟服务器环境反馈 ---
        hour = current_time / 3600
        if 3 <= hour <= 5:
            # 模拟风控期间：服务器响应极慢且不稳定
            actual_latency = random.uniform(3.5, 6.0)
        else:
            # 正常期间：响应快速
            actual_latency = random.uniform(0.5, 1.8)
            
        # 1. 贝叶斯学习环境
        gov.observe_and_update(actual_latency)
        
        # 2. 获取混沌延迟
        delay = gov.get_next_delay()
        current_time += delay
        if current_time > duration_secs: break
        
        total_jobs += 1
        
        # 记录状态
        stats.append({
            'time': current_time,
            'risk': gov.risk_level,
            'slot': int(current_time // 60)
        })

    # --- 可视化：任务密度与风险水位 ---
    slots_count = duration_hours * 60 # 1分钟一个槽位
    density_map = [0] * slots_count
    risk_map = [0.0] * slots_count
    
    for s in stats:
        if s['slot'] < slots_count:
            density_map[s['slot']] += 1
            risk_map[s['slot']] = s['risk']

    print(f"\n📊 战术呼吸感 + 贝叶斯风险监控图 (每列1分钟)")
    print("   [ █ = 任务密度 | 🌊 = 风险水位 ]")
    print("-" * (slots_count + 15))
    
    # 打印密度图
    for h in range(3, 0, -1):
        line = f"密度 {h:d} |"
        for val in density_map:
            if val >= h: line += "█"
            else: line += " "
        print(line)
        
    # 打印风险图
    line = "风险线 |"
    for r in risk_map:
        if r > 0.7: line += "🔥" # 极高风险
        elif r > 0.4: line += "🌊" # 中高风险
        elif r > 0.1: line += "░" # 低风险
        else: line += " "
    print(line)
    
    print("-" * (slots_count + 15))
    print(f"📈 总结: 8小时完成 {total_jobs} 任务 | 峰值风险 {max(risk_map):.1%}")

if __name__ == "__main__":
    simulate_v7_bayesian()
