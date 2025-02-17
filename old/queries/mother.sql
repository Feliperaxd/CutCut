-- Funcs
CREATE OR REPLACE FUNCTION prevent_id_update()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id IS DISTINCT FROM OLD.id THEN
        RAISE EXCEPTION 'Cannot update the id column';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION prevent_creation_date_update()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.creation_date IS DISTINCT FROM OLD.creation_date THEN
        RAISE EXCEPTION 'Cannot update the creation_date column';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_update_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_date := NOW();
    RETURN NEW;           
END;
$$ LANGUAGE plpgsql;


-- Creating table users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER prevent_id_update_trigger_users
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION prevent_id_update();

CREATE TRIGGER prevent_creation_date_update_trigger_users
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION prevent_creation_date_update();

CREATE TRIGGER set_new_update_date_trigger_users
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_update_date();


-- Creating table accesses
CREATE TABLE accesses (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TRIGGER prevent_id_update_trigger_accesses
BEFORE UPDATE ON accesses
FOR EACH ROW
EXECUTE FUNCTION prevent_id_update();

CREATE TRIGGER prevent_creation_date_update_trigger_accesses
BEFORE UPDATE ON accesses
FOR EACH ROW
EXECUTE FUNCTION prevent_creation_date_update();


-- Creating table videos
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(100) NOT NULL,
    url VARCHAR(500) NOT NULL,
    title VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    view_count INT NOT NULL,
    channel_tag VARCHAR(100) NOT NULL,
    channel_url VARCHAR(500) NOT NULL,
    channel_name VARCHAR(255) NOT NULL,
    thumbnail_url VARCHAR(500) NOT NULL,
    channel_is_verified BOOLEAN NOT NULL,
    access_count INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER prevent_id_update_trigger_videos
BEFORE UPDATE ON videos
FOR EACH ROW
EXECUTE FUNCTION prevent_id_update();

CREATE TRIGGER prevent_creation_date_update_trigger_videos
BEFORE UPDATE ON videos
FOR EACH ROW
EXECUTE FUNCTION prevent_creation_date_update();

CREATE TRIGGER set_new_update_date_trigger_videos
BEFORE UPDATE ON videos
FOR EACH ROW
EXECUTE FUNCTION set_update_date();


-- Creating table searches
CREATE TABLE searches (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    query VARCHAR(500) NOT NULL,
    max_results INT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TRIGGER prevent_id_update_trigger_searches
BEFORE UPDATE ON searches
FOR EACH ROW
EXECUTE FUNCTION prevent_id_update();

CREATE TRIGGER prevent_creation_date_update_trigger_searches
BEFORE UPDATE ON searches
FOR EACH ROW
EXECUTE FUNCTION prevent_creation_date_update();


-- Creating table cart_items
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    video_id INT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
);

CREATE TRIGGER prevent_id_update_trigger_cart_items
BEFORE UPDATE ON cart_items
FOR EACH ROW
EXECUTE FUNCTION prevent_id_update();

CREATE TRIGGER prevent_creation_date_update_trigger_cart_items
BEFORE UPDATE ON cart_items
FOR EACH ROW
EXECUTE FUNCTION prevent_creation_date_update();
