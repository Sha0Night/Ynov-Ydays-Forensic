CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(150),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sites (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    name VARCHAR(100) NOT NULL,
    location VARCHAR(150),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(id),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    serial_number VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE measurements (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id),
    measured_at TIMESTAMPTZ NOT NULL,
    value_celsius NUMERIC(5,2) NOT NULL,
    raw_payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO clients (name, contact_email)
VALUES ('ClimIT Client Demo', 'client.demo@climit.local');

INSERT INTO sites (client_id, name, location)
VALUES (1, 'Site 1', 'Montpellier - Bâtiment A');

INSERT INTO sensors (site_id, name, type, serial_number)
VALUES (1, 'Sensor 1 - Salle Serveur', 'temperature', 'SIM-0001');
