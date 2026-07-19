-- =====================================================
-- Davinci Physiotherapy - Database Schema
-- =====================================================

CREATE DATABASE IF NOT EXISTS davinci_physiotherapy
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE davinci_physiotherapy;

-- -----------------------------------------------------
-- Table: admins
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'admin',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_admin_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table: services
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100) DEFAULT 'fa-solid fa-hand-holding-medical',
    image VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_service_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table: appointments
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(120),
    age INT,
    gender VARCHAR(10),
    service_id INT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    address VARCHAR(255),
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_appt_status (status),
    INDEX idx_appt_created (created_at),
    CONSTRAINT fk_appointment_service FOREIGN KEY (service_id)
        REFERENCES services(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table: contact_messages
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_contact_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table: testimonials
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(150) NOT NULL,
    designation VARCHAR(150),
    review TEXT NOT NULL,
    rating INT DEFAULT 5,
    image VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_testimonial_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table: settings
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clinic_name VARCHAR(150) DEFAULT 'Davinci Physiotherapy',
    phone VARCHAR(20),
    email VARCHAR(120),
    address VARCHAR(255),
    google_map TEXT,
    facebook VARCHAR(255),
    instagram VARCHAR(255),
    whatsapp VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Seed data
-- =====================================================

-- NOTE: Do not insert an admin row here with a hardcoded password hash.
-- After importing this schema, create your first admin account by running:
--   python create_admin.py
-- (this uses Werkzeug to generate a proper password hash for you)

INSERT INTO services (title, description, icon, status) VALUES
('Orthopedic Physiotherapy', 'Post-surgical rehab, joint & muscle pain management, arthritis care.', 'fa-solid fa-bone', 'active'),
('Respiratory Physiotherapy', 'Chest physiotherapy, breathing exercises, post-COVID rehabilitation.', 'fa-solid fa-lungs', 'active'),
('Neurological Rehabilitation', 'Stroke rehab, Parkinson''s care, nerve injuries, balance & coordination training.', 'fa-solid fa-brain', 'active'),
('Pediatric Physiotherapy', 'Developmental delays, cerebral palsy, posture correction.', 'fa-solid fa-child', 'active'),
('Geriatric Care', 'Age-related mobility issues, falls prevention, strength & balance training.', 'fa-solid fa-person-cane', 'active');

INSERT INTO settings (clinic_name, phone, email, address, google_map, facebook, instagram, whatsapp) VALUES
('Davinci Physiotherapy', '90251 00053', 'davinciphysiotherapy@gmail.com',
 'PA 9 Block, Police Quarters TNPHC, Melakottaiyur, Kandigai, Off Vandalur Kelambakkam Road, Chennai - 600127',
 '', '', '', '919025100053');

INSERT INTO testimonials (patient_name, designation, review, rating, status) VALUES
('Kavitha R.', 'Homemaker', 'The home visit physiotherapy service transformed my recovery after knee surgery. Truly professional and caring team.', 5, 'active'),
('Suresh Kumar', 'Retired Engineer', 'Excellent geriatric care. The therapist was patient and skilled. Highly recommend Davinci Physiotherapy.', 5, 'active'),
('Anitha M.', 'Working Professional', 'Convenient, compassionate, and effective. My back pain has improved significantly within a few sessions.', 5, 'active');
