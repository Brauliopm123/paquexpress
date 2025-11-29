-- Script de Creación de Base de Datos para Paquexpress S.A. de C.V.

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS paquexpress;
USE paquexpress;

-- Tabla de Agentes
CREATE TABLE agentes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Paquetes 
CREATE TABLE paquetes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  paquete_id VARCHAR(100) NOT NULL UNIQUE,
  direccion VARCHAR(255) NOT NULL,
  destinatario VARCHAR(150),
  estado ENUM('pendiente','en_ruta','entregado','fallido') DEFAULT 'pendiente',
  asignado_a INT NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (asignado_a) REFERENCES agentes(id)
);
-- Tabla de Entregas
CREATE TABLE entregas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  paquete_id INT NOT NULL,
  agente_id INT NOT NULL,
  url_foto_evidencia VARCHAR(500),
  latitud DECIMAL(10,7),
  longitud DECIMAL(10,7),
  fecha_entrega TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (paquete_id) REFERENCES paquetes(id),
  FOREIGN KEY (agente_id) REFERENCES agentes(id)
);

INSERT INTO agentes (nombre, email, password_hash) 
VALUES ('Pedro', 'pedro@paquexpress.com', '$2b$12$f0i/3y0n8s6L6F4m2L8mG.V0z8k9w7Q5A4S2D1F9G8H7J6K5L4M3N2O1P0R9S8T7U6V5W4X3Y2Z1'); 

INSERT INTO Paquetes (paquete_id, direccion, asignado_a) 
VALUES 
('BPM-1524', 'Avenida Soleda #954, España', 1),
('BPM-9752', 'Calle Falsa #123, Ciudad de México', 1);