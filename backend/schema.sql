-- MealMate（餐伴）数据库 Schema
-- SQLite

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone VARCHAR(20) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    avatar TEXT,
    taste_tags TEXT,               -- JSON数组: ["辣","低脂","爱吃鸡"]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 菜品池表（推荐候选）
CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    cuisine VARCHAR(20),           -- 川菜/粤菜/湘菜/日料/西餐/东南亚
    tags TEXT,                     -- JSON数组: ["辣","下饭","清淡"]
    reference_price REAL,          -- 参考价格（元）
    prep_time INTEGER,             -- 预计制作/送达时间（分钟）
    calories INTEGER,              -- 热量（千卡）
    image_url TEXT,
    is_active INTEGER DEFAULT 1,   -- 是否启用 1=启用 0=禁用
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 饮食记录表
CREATE TABLE IF NOT EXISTS meal_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    dish_name VARCHAR(100) NOT NULL,
    meal_type VARCHAR(10) NOT NULL, -- 早餐/午餐/晚餐/下午茶/夜宵
    location_name VARCHAR(200),
    latitude REAL,
    longitude REAL,
    cost REAL,                     -- 花费金额（元）
    calories INTEGER,              -- 热量（千卡）
    photo_url TEXT,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    tags TEXT,                     -- JSON数组: ["面食","快捷"]
    meal_date DATE NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 用户反馈表（用于推荐优化）
CREATE TABLE IF NOT EXISTS user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    action VARCHAR(10) NOT NULL,   -- like / dislike / accept
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_meal_records_user_id ON meal_records(user_id);
CREATE INDEX IF NOT EXISTS idx_meal_records_meal_date ON meal_records(meal_date);
CREATE INDEX IF NOT EXISTS idx_meal_records_user_date ON meal_records(user_id, meal_date);
CREATE INDEX IF NOT EXISTS idx_user_feedback_user_dish ON user_feedback(user_id, dish_id);
CREATE INDEX IF NOT EXISTS idx_dishes_cuisine ON dishes(cuisine);
