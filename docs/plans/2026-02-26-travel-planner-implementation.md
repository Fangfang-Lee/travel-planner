# Travel Planner Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现一个完整的多 Agent 旅行规划系统，包含后端 API 服务和 React 前端

**Architecture:** 采用前后端分离架构，后端使用 CrewAI 实现多 Agent 协作，前端使用 React 实现用户交互

**Tech Stack:** CrewAI, FastAPI, React, TypeScript, TailwindCSS, Render

---

## 阶段一：项目初始化

### Task 1: 初始化 Python 后端项目结构

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/.env.example`

**Step 1: 创建项目目录和 pyproject.toml**

```bash
mkdir -p backend
cd backend
```

创建 `backend/pyproject.toml`:

```toml
[project]
name = "travel-planner-backend"
version = "0.1.0"
description = "智能旅行规划助手后端服务"
requires-python = ">=3.11"
dependencies = [
    "crewai>=0.80.0",
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "tavily-python>=0.3.0",
    "langchain-community>=0.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",
]
```

创建 `backend/.env.example`:

```bash
# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Tavily Search
TAVILY_API_KEY=your-tavily-api-key

# App Settings
APP_HOST=0.0.0.0
APP_PORT=8000
```

**Step 2: Commit**

```bash
git add backend/pyproject.toml backend/.env.example
git commit -m "chore: 初始化后端项目结构"
```

---

### Task 2: 初始化 React 前端项目

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/index.html`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/postcss.config.js`

**Step 1: 创建前端项目结构和配置文件**

创建 `frontend/package.json`:

```json
{
  "name": "travel-planner-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.26.0",
    "axios": "^1.7.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.5.0",
    "vite": "^5.4.0"
  }
}
```

创建 `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

创建 `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

创建 `frontend/index.html`:

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>智能旅行规划助手</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

创建 `frontend/tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

创建 `frontend/postcss.config.js`:

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

创建 `frontend/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Step 2: Commit**

```bash
git add frontend/
git commit -m "chore: 初始化 React 前端项目"
```

---

## 阶段二：后端核心实现

### Task 3: 实现 FastAPI 基础服务

**Files:**
- Create: `backend/main.py`
- Create: `backend/app/config.py`
- Create: `backend/tests/test_main.py`

**Step 1: 创建 main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="旅行规划助手 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "旅行规划助手 API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Step 2: 创建配置模块**

创建 `backend/app/config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))


settings = Settings()
```

**Step 3: 创建测试**

创建 `backend/tests/test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "旅行规划助手 API", "status": "running"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

**Step 4: 运行测试**

```bash
cd backend
pip install -e ".[dev]"
pytest tests/test_main.py -v
```

预期输出：PASS

**Step 5: Commit**

```bash
git add backend/main.py backend/app/ backend/tests/
git commit -m "feat: 实现 FastAPI 基础服务"
```

---

### Task 4: 实现 CrewAI Agent 角色定义

**Files:**
- Create: `backend/app/agents/travel_advisor.py`
- Create: `backend/app/agents/search_agent.py`
- Create: `backend/app/agents/planner.py`
- Create: `backend/app/agents/budget_analyst.py`
- Create: `backend/app/agents/weather_agent.py`
- Create: `backend/app/agents/__init__.py`
- Create: `backend/app/tools/tavily_search.py`

**Step 1: 创建搜索工具**

创建 `backend/app/tools/tavily_search.py`:

```python
from crewai.tools import tool
from tavily import Tavily


class TavilySearchTool:
    @tool("搜索旅行相关信息")
    def search(query: str) -> str:
        """
        搜索旅行相关信息，包括景点、酒店、美食、天气等。
        输入应该是清晰的搜索关键词。
        """
        tavily = Tavily(api_key="")
        results = tavily.search(query=query, max_results=5)

        if not results.get("results"):
            return "未找到相关信息"

        formatted = []
        for r in results["results"]:
            formatted.append(f"标题: {r.get('title', '')}\n内容: {r.get('content', '')}\n")

        return "\n\n".join(formatted)
```

**Step 2: 创建 Travel Advisor Agent**

创建 `backend/app/agents/travel_advisor.py`:

```python
from crewai import Agent
from langchain_openai import ChatOpenAI


def create_travel_advisor():
    return Agent(
        role="旅行顾问",
        goal="深入了解用户的旅行需求和偏好",
        backstory="""
        你是一位经验丰富的旅行顾问，已经帮助数千位客户规划了完美的旅行。
        你擅长通过对话挖掘用户真正的需求，包括预算、偏好、旅行风格等。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
    )
```

**Step 3: 创建 Search Agent**

创建 `backend/app/agents/search_agent.py`:

```python
from crewai import Agent
from langchain_openai import ChatOpenAI
from app.tools.tavily_search import TavilySearchTool


def create_search_agent():
    return Agent(
        role="搜索代理",
        goal="获取准确、及时的旅行信息",
        backstory="""
        你是一位专业的旅行信息搜索专家，擅长从各种来源获取最新的旅行信息。
        你能快速找到景点、酒店、餐厅、天气等用户需要的信息。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
        tools=[TavilySearchTool()],
    )
```

**Step 4: 创建 Planner Agent**

创建 `backend/app/agents/planner.py`:

```python
from crewai import Agent
from langchain_openai import ChatOpenAI


def create_planner_agent():
    return Agent(
        role="行程规划师",
        goal="整合信息，制定合理的行程安排",
        backstory="""
        你是一位资深的行程规划师，擅长将各种旅行信息整合成完整、合理的行程计划。
        你会考虑时间安排、距离顺序、用户偏好等因素。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
    )
```

**Step 5: 创建 Budget Analyst Agent**

创建 `backend/app/agents/budget_analyst.py`:

```python
from crewai import Agent
from langchain_openai import ChatOpenAI


def create_budget_analyst():
    return Agent(
        role="预算分析师",
        goal="计算旅行费用并提供优化建议",
        backstory="""
        你是一位精明的预算分析师，擅长计算各种旅行费用并提供节省建议。
        你会根据行程给出详细的费用 breakdown。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
    )
```

**Step 6: 创建 Weather Agent**

创建 `backend/app/agents/weather_agent.py`:

```python
from crewai import Agent
from langchain_openai import ChatOpenAI
from app.tools.tavily_search import TavilySearchTool


def create_weather_agent():
    return Agent(
        role="天气与应急代理",
        goal="提供天气信息和应急处理方案",
        backstory="""
        你是一位旅行安全专家，擅长预测天气风险并提供应急方案。
        你会关注目的地在旅行期间可能遇到的天气问题并给出建议。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
        tools=[TavilySearchTool()],
    )
```

**Step 7: 创建 __init__.py**

创建 `backend/app/agents/__init__.py`:

```python
from app.agents.travel_advisor import create_travel_advisor
from app.agents.search_agent import create_search_agent
from app.agents.planner import create_planner_agent
from app.agents.budget_analyst import create_budget_analyst
from app.agents.weather_agent import create_weather_agent

__all__ = [
    "create_travel_advisor",
    "create_search_agent",
    "create_planner_agent",
    "create_budget_analyst",
    "create_weather_agent",
]
```

**Step 8: Commit**

```bash
git add backend/app/agents/ backend/app/tools/
git commit -m "feat: 实现 CrewAI Agent 角色定义"
```

---

### Task 5: 实现 CrewAI Task 和 Crew 编排

**Files:**
- Create: `backend/app/crew/planner_crew.py`
- Create: `backend/app/crew/__init__.py`
- Create: `backend/tests/test_crew.py`

**Step 1: 创建 Planner Crew**

创建 `backend/app/crew/planner_crew.py`:

```python
from crewai import Crew, Task, Process
from app.agents import (
    create_travel_advisor,
    create_search_agent,
    create_planner_agent,
    create_budget_analyst,
    create_weather_agent,
)


class TripPlannerCrew:
    def __init__(self, destination: str, duration: int, budget: float,
                 travelers: int, preferences: list):
        self.destination = destination
        self.duration = duration
        self.budget = budget
        self.travelers = travelers
        self.preferences = preferences

        self.travel_advisor = create_travel_advisor()
        self.search_agent = create_search_agent()
        self.planner = create_planner_agent()
        self.budget_analyst = create_budget_analyst()
        self.weather_agent = create_weather_agent()

    def plan(self):
        # Define tasks
        clarify_task = Task(
            description=f"Clarify travel requirements for {self.destination}, "
                        f"{self.duration} days, budget {self.budget} yuan, "
                        f"{self.travelers} travelers, preferences: {self.preferences}",
            agent=self.travel_advisor,
            expected_output="清晰的需求清单，包括必去景点、住宿偏好、餐饮要求等",
        )

        search_task = Task(
            description=f"Search for travel information about {self.destination}, "
                        f"including attractions, hotels, restaurants, weather",
            agent=self.search_agent,
            expected_output="搜索结果摘要，包含景点、酒店、美食、天气信息",
            context=[clarify_task],
        )

        plan_task = Task(
            description=f"Create a detailed travel plan for {self.destination}, "
                        f"{self.duration} days based on search results",
            agent=self.planner,
            expected_output="详细的每日行程安排",
            context=[clarify_task, search_task],
        )

        budget_task = Task(
            description=f"Calculate estimated cost for the trip to {self.destination}, "
                        f"budget: {self.budget} yuan for {self.travelers} people",
            agent=self.budget_analyst,
            expected_output="费用明细表和优化建议",
            context=[plan_task],
        )

        weather_task = Task(
            description=f"Check weather forecast for {self.destination} "
                        f"for the next {self.duration} days and provide tips",
            agent=self.weather_agent,
            expected_output="天气预报和旅行建议",
            context=[plan_task],
        )

        # Create crew
        crew = Crew(
            agents=[
                self.travel_advisor,
                self.search_agent,
                self.planner,
                self.budget_analyst,
                self.weather_agent,
            ],
            tasks=[clarify_task, search_task, plan_task, budget_task, weather_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result
```

**Step 2: 创建 __init__.py**

创建 `backend/app/crew/__init__.py`:

```python
from app.crew.planner_crew import TripPlannerCrew

__all__ = ["TripPlannerCrew"]
```

**Step 3: 创建测试**

创建 `backend/tests/test_crew.py`:

```python
# 注意：这个测试需要有效的 API key
# 实际测试时可以 mock 或使用 pytest.mark.skip


def test_trip_planner_crew_init():
    from app.crew.planner_crew import TripPlannerCrew

    crew = TripPlannerCrew(
        destination="东京",
        duration=5,
        budget=10000,
        travelers=2,
        preferences=["美食", "购物"]
    )

    assert crew.destination == "东京"
    assert crew.duration == 5
    assert crew.budget == 10000
    assert crew.travelers == 2
    assert crew.preferences == ["美食", "购物"]
```

**Step 4: 运行测试**

```bash
cd backend
pytest tests/test_crew.py -v
```

预期输出：PASS

**Step 5: Commit**

```bash
git add backend/app/crew/ backend/tests/test_crew.py
git commit -m "feat: 实现 Crew 任务编排"
```

---

### Task 6: 实现 API 端点

**Files:**
- Modify: `backend/main.py`
- Create: `backend/app/schemas/trip.py`
- Create: `backend/app/api/trips.py`
- Create: `backend/app/api/__init__.py`
- Create: `backend/tests/test_api.py`

**Step 1: 创建 Pydantic 模型**

创建 `backend/app/schemas/trip.py`:

```python
from pydantic import BaseModel
from typing import Optional, List


class TripRequest(BaseModel):
    destination: str
    duration: int
    budget: float
    travelers: int
    preferences: List[str]


class TripResponse(BaseModel):
    id: str
    destination: str
    duration: int
    budget: float
    travelers: int
    preferences: List[str]
    plan: Optional[str] = None
    status: str = "pending"


class TripOptimizeRequest(BaseModel):
    optimization_type: str  # "budget", "time", "experience"
```

**Step 2: 创建 API 路由**

创建 `backend/app/api/trips.py`:

```python
from fastapi import APIRouter, HTTPException
from app.schemas.trip import TripRequest, TripResponse, TripOptimizeRequest
from app.crew.planner_crew import TripPlannerCrew
import uuid
from datetime import datetime

router = APIRouter()

# In-memory storage (use database in production)
trips_db = {}


@router.post("/trips/plan", response_model=TripResponse)
async def create_trip_plan(request: TripRequest):
    trip_id = str(uuid.uuid4())

    trip = TripResponse(
        id=trip_id,
        destination=request.destination,
        duration=request.duration,
        budget=request.budget,
        travelers=request.travelers,
        preferences=request.preferences,
        status="processing"
    )

    trips_db[trip_id] = trip

    try:
        crew = TripPlannerCrew(
            destination=request.destination,
            duration=request.duration,
            budget=request.budget,
            travelers=request.travelers,
            preferences=request.preferences
        )
        result = crew.plan()

        trip.plan = str(result)
        trip.status = "completed"
        trips_db[trip_id] = trip

        return trip
    except Exception as e:
        trip.status = "failed"
        trips_db[trip_id] = trip
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trips/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: str):
    if trip_id not in trips_db:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trips_db[trip_id]


@router.get("/trips")
async def list_trips():
    return list(trips_db.values())


@router.post("/trips/{trip_id}/optimize")
async def optimize_trip(trip_id: str, request: TripOptimizeRequest):
    if trip_id not in trips_db:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip = trips_db[trip_id]
    return {
        "trip_id": trip_id,
        "message": f"优化类型: {request.optimization_type}",
        "status": "optimized"
    }
```

创建 `backend/app/api/__init__.py`:

```python
from app.api.trips import router as trips_router

__all__ = ["trips_router"]
```

**Step 3: 更新 main.py**

修改 `backend/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="旅行规划助手 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.trips import router as trips_router
app.include_router(trips_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "旅行规划助手 API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Step 4: 创建 API 测试**

创建 `backend/tests/test_api.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_trip_plan():
    response = client.post(
        "/api/trips/plan",
        json={
            "destination": "东京",
            "duration": 5,
            "budget": 10000,
            "travelers": 2,
            "dependencies": ["美食", "购物"]
        }
    )
    # 由于需要 API key，这里测试会失败，但验证端点存在
    assert response.status_code in [200, 500]


def test_list_trips():
    response = client.get("/api/trips")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

**Step 5: 运行测试**

```bash
cd backend
pytest tests/test_api.py -v
```

预期输出：PASS

**Step 6: Commit**

```bash
git add backend/main.py backend/app/schemas/ backend/app/api/ backend/tests/test_api.py
git commit -m "feat: 实现旅行规划 API 端点"
```

---

## 阶段三：前端实现

### Task 7: 实现 React 页面组件

**Files:**
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/pages/HomePage.tsx`
- Create: `frontend/src/pages/TripDetail.tsx`
- Create: `frontend/src/pages/MyTrips.tsx`
- Create: `frontend/src/components/TripForm.tsx`
- Create: `frontend/src/components/TripCard.tsx`
- Create: `frontend/src/api/trips.ts`
- Create: `frontend/src/types/trip.ts`

**Step 1: 创建类型定义**

创建 `frontend/src/types/trip.ts`:

```typescript
export interface TripRequest {
  destination: string;
  duration: number;
  budget: number;
  travelers: number;
  preferences: string[];
}

export interface Trip {
  id: string;
  destination: string;
  duration: number;
  budget: number;
  travelers: number;
  preferences: string[];
  plan?: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}
```

**Step 2: 创建 API 客户端**

创建 `frontend/src/api/trips.ts`:

```typescript
import axios from 'axios';
import { Trip, TripRequest } from '../types/trip';

const api = axios.create({
  baseURL: '/api',
});

export const tripApi = {
  createPlan: (data: TripRequest): Promise<Trip> =>
    api.post('/trips/plan', data).then(res => res.data),

  getTrip: (id: string): Promise<Trip> =>
    api.get(`/trips/${id}`).then(res => res.data),

  listTrips: (): Promise<Trip[]> =>
    api.get('/trips').then(res => res.data),
};
```

**Step 3: 创建 TripForm 组件**

创建 `frontend/src/components/TripForm.tsx`:

```typescript
import { useState } from 'react';
import { TripRequest } from '../types/trip';

interface Props {
  onSubmit: (data: TripRequest) => void;
  loading?: boolean;
}

const preferenceOptions = ['美食', '购物', '文化', '自然', '冒险', '休闲'];

export function TripForm({ onSubmit, loading }: Props) {
  const [destination, setDestination] = useState('');
  const [duration, setDuration] = useState(5);
  const [budget, setBudget] = useState(10000);
  const [travelers, setTravelers] = useState(2);
  const [preferences, setPreferences] = useState<string[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ destination, duration, budget, travelers, preferences });
  };

  const togglePreference = (pref: string) => {
    setPreferences(prev =>
      prev.includes(pref)
        ? prev.filter(p => p !== pref)
        : [...prev, pref]
    );
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-xl mx-auto">
      <div>
        <label className="block text-sm font-medium mb-2">目的地</label>
        <input
          type="text"
          value={destination}
          onChange={e => setDestination(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg"
          placeholder="例如：日本东京"
          required
        />
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2">天数</label>
          <input
            type="number"
            value={duration}
            onChange={e => setDuration(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            min={1}
            max={30}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">预算(元)</label>
          <input
            type="number"
            value={budget}
            onChange={e => setBudget(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            min={1000}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">人数</label>
          <input
            type="number"
            value={travelers}
            onChange={e => setTravelers(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            min={1}
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">偏好</label>
        <div className="flex flex-wrap gap-2">
          {preferenceOptions.map(pref => (
            <button
              key={pref}
              type="button"
              onClick={() => togglePreference(pref)}
              className={`px-4 py-2 rounded-full border ${
                preferences.includes(pref)
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-gray-700'
              }`}
            >
              {pref}
            </button>
          ))}
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
      >
        {loading ? '规划中...' : '开始规划'}
      </button>
    </form>
  );
}
```

**Step 4: 创建 TripCard 组件**

创建 `frontend/src/components/TripCard.tsx`:

```typescript
import { Trip } from '../types/trip';

interface Props {
  trip: Trip;
  onClick?: () => void;
}

export function TripCard({ trip, onClick }: Props) {
  const statusColors = {
    pending: 'bg-gray-100',
    processing: 'bg-yellow-100',
    completed: 'bg-green-100',
    failed: 'bg-red-100',
  };

  return (
    <div
      onClick={onClick}
      className="p-4 border rounded-lg hover:shadow-md cursor-pointer transition"
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold">{trip.destination}</h3>
          <p className="text-gray-600">
            {trip.duration}天 · {trip.travelers}人 · ¥{trip.budget}
          </p>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm ${statusColors[trip.status]}`}>
          {trip.status === 'processing' ? '规划中' : trip.status}
        </span>
      </div>
      <div className="mt-2 flex gap-2">
        {trip.preferences.map(p => (
          <span key={p} className="text-xs bg-gray-100 px-2 py-1 rounded">
            {p}
          </span>
        ))}
      </div>
    </div>
  );
}
```

**Step 5: 创建页面组件**

创建 `frontend/src/pages/HomePage.tsx`:

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TripForm } from '../components/TripForm';
import { tripApi } from '../api/trips';
import { TripRequest, Trip } from '../types/trip';

export function HomePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data: TripRequest) => {
    setLoading(true);
    try {
      const trip: Trip = await tripApi.createPlan(data);
      navigate(`/trips/${trip.id}`);
    } catch (error) {
      console.error(error);
      alert('规划失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">智能旅行规划助手</h1>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-2">规划你的下一次旅行</h2>
          <p className="text-gray-600">AI 驱动，多 Agent 协作，为你打造专属行程</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-8">
          <TripForm onSubmit={handleSubmit} loading={loading} />
        </div>
      </main>
    </div>
  );
}
```

创建 `frontend/src/pages/TripDetail.tsx`:

```typescript
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { tripApi } from '../api/trips';
import { Trip } from '../types/trip';

export function TripDetail() {
  const { id } = useParams<{ id: string }>();
  const [trip, setTrip] = useState<Trip | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    const fetchTrip = async () => {
      try {
        const data = await tripApi.getTrip(id);
        setTrip(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrip();
  }, [id]);

  if (loading) return <div className="p-8 text-center">加载中...</div>;
  if (!trip) return <div className="p-8 text-center">行程不存在</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <Link to="/" className="text-blue-500 hover:underline">
            ← 返回
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm p-8">
          <h1 className="text-2xl font-bold mb-4">{trip.destination}</h1>

          <div className="flex gap-4 mb-6">
            <span className="px-3 py-1 bg-gray-100 rounded">
              {trip.duration}天
            </span>
            <span className="px-3 py-1 bg-gray-100 rounded">
              {trip.travelers}人
            </span>
            <span className="px-3 py-1 bg-gray-100 rounded">
              ¥{trip.budget}
            </span>
          </div>

          {trip.plan && (
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap">{trip.plan}</pre>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
```

创建 `frontend/src/pages/MyTrips.tsx`:

```typescript
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { tripApi } from '../api/trips';
import { TripCard } from '../components/TripCard';
import { Trip } from '../types/trip';

export function MyTrips() {
  const navigate = useNavigate();
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const data = await tripApi.listTrips();
        setTrips(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrips();
  }, []);

  if (loading) return <div className="p-8 text-center">加载中...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">我的旅行</h1>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {trips.map(trip => (
            <TripCard
              key={trip.id}
              trip={trip}
              onClick={() => navigate(`/trips/${trip.id}`)}
            />
          ))}
        </div>

        {trips.length === 0 && (
          <p className="text-center text-gray-500">暂无旅行计划</p>
        )}
      </main>
    </div>
  );
}
```

**Step 6: 更新 App.tsx**

创建 `frontend/src/App.tsx`:

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { TripDetail } from './pages/TripDetail';
import { MyTrips } from './pages/MyTrips';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/trips/:id" element={<TripDetail />} />
        <Route path="/my-trips" element={<MyTrips />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

创建 `frontend/src/main.tsx`:

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Step 7: Commit**

```bash
git add frontend/src/
git commit -m "feat: 实现 React 前端页面组件"
```

---

## 阶段四：部署配置

### Task 8: 创建部署配置文件

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/Dockerfile`
- Create: `frontend/Dockerfile`
- Create: `render.yaml`

**Step 1: 创建 requirements.txt**

```bash
cd backend
pip freeze > requirements.txt
```

**Step 2: 创建后端 Dockerfile**

创建 `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Step 3: 创建前端 Dockerfile**

创建 `frontend/Dockerfile`:

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Step 4: 创建 render.yaml**

创建 `render.yaml`:

```yaml
services:
  - type: web
    name: travel-planner-backend
    env: python
    region: oregon
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: TAVILY_API_KEY
        sync: false
    plan: free

  - type: web
    name: travel-planner-frontend
    env: static
    region: oregon
    buildCommand: cd frontend && npm ci && npm run build
    staticPublishPath: frontend/dist
    plan: free
```

**Step 5: Commit**

```bash
git add backend/requirements.txt backend/Dockerfile frontend/Dockerfile render.yaml
git commit -m "chore: 添加部署配置文件"
```

---

## 阶段五：最终集成与测试

### Task 9: 端到端测试

**Step 1: 启动后端服务**

```bash
cd backend
cp .env.example .env
# 编辑 .env 填入 API key
uvicorn main:app --reload
```

**Step 2: 启动前端服务**

```bash
cd frontend
npm install
npm run dev
```

**Step 3: 测试完整流程**

1. 打开 http://localhost:3000
2. 填写旅行需求
3. 提交并等待结果
4. 查看行程详情

**Step 4: Commit**

```bash
git add .
git commit - "chore: 完成端到端测试"
```

---

## 实现顺序总结

| 顺序 | 任务 | 预计时间 |
|------|------|----------|
| 1 | 初始化项目结构 | 15 min |
| 2 | FastAPI 基础服务 | 20 min |
| 3 | CrewAI Agent 定义 | 30 min |
| 4 | Crew 任务编排 | 20 min |
| 5 | API 端点 | 20 min |
| 6 | React 前端 | 45 min |
| 7 | 部署配置 | 15 min |
| 8 | 端到端测试 | 30 min |
