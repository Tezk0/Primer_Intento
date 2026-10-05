-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema intento_certificacion
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema intento_certificacion
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `intento_certificacion` DEFAULT CHARACTER SET utf8 ;
USE `intento_certificacion` ;

-- -----------------------------------------------------
-- Table `intento_certificacion`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `intento_certificacion`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(80) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `intento_certificacion`.`peliculas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `intento_certificacion`.`peliculas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_pelicula` VARCHAR(45) NOT NULL,
  `director` VARCHAR(45) NOT NULL,
  `fecha_estreno` VARCHAR(45) NOT NULL,
  `sinopsis` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`, `usuario_id`),
  INDEX `fk_peliculas_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_peliculas_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `intento_certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `intento_certificacion`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `intento_certificacion`.`comentarios` (
  `usuarios_id` INT NOT NULL,
  `peliculas_id` INT NOT NULL,
  `comentario` TEXT NOT NULL,
  PRIMARY KEY (`usuarios_id`, `peliculas_id`),
  INDEX `fk_usuarios_has_peliculas_peliculas1_idx` (`peliculas_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_peliculas_usuarios_idx` (`usuarios_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_peliculas_usuarios`
    FOREIGN KEY (`usuarios_id`)
    REFERENCES `intento_certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_peliculas_peliculas1`
    FOREIGN KEY (`peliculas_id`)
    REFERENCES `intento_certificacion`.`peliculas` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
