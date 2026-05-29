CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'client')),
    client_name TEXT
);

-- admin par défaut : admin@example.com / Admin!2026
INSERT INTO users (email, password_hash, role, client_name)
VALUES (
    'admin@example.com',
    -- hash bcrypt de Admin!2026
    '$2b$12$LzZJYFvV1b3c4.CgJXx7ueL1bp/yWfvC5r.Ut9P2CXo4dc8oPwLA6',
    'admin',
    'ClimIT Admin'
)
ON CONFLICT (email) DO NOTHING;
