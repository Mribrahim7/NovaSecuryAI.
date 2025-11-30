from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()

attack_logs = []
blocked_ips = set()

# --- MODELS ---
class AttackEvent(BaseModel):
    ip: str
    attack_type: str
    timestamp: str

# --- AI RISK ENGINE ---
def ai_risk_score(attack_type: str):
    scores = {
        "DDoS": 0.9,
        "PortScan": 0.6,
        "SQLi": 0.95,
        "Bruteforce": 0.7
    }
    return scores.get(attack_type, 0.2)

# --- DEFENSE ACTIONS ---
def apply_defense(ip, attack_type):
    res = []
    # Alert
    res.append({
        "action": "alert",
        "msg": f"Security alert: {attack_type} from {ip}",
        "time": datetime.now().isoformat()
    })

    # Rate limiting
    res.append({
        "action": "rate_limit",
        "limit": "100 req/min",
        "time": datetime.now().isoformat()
    })

    # IP Block
    blocked_ips.add(ip)
    res.append({
        "action": "ip_block",
        "ip": ip,
        "time": datetime.now().isoformat()
    })

    return res

# --- API ENDPOINTS ---
@app.post("/simulate_attack")
def simulate_attack(event: AttackEvent):
    score = ai_risk_score(event.attack_type)

    attack_logs.append({
        "ip": event.ip,
        "type": event.attack_type,
        "time": event.timestamp,
        "risk": score
    })

    defense = apply_defense(event.ip, event.attack_type)

    return {
        "status": "processed",
        "risk_score": score,
        "defense": defense
    }

@app.get("/dashboard")
def get_dashboard():
    cpu = round(random.uniform(3.5, 15.0), 1)
    ram = round(random.uniform(40, 90), 1)

    return {
        "cpu": cpu,
        "ram": ram,
        "attacks": len(attack_logs),
        "blocked_ips": len(blocked_ips),
        "recent": attack_logs[-5:]
    }
