CREATE TABLE `wzz_city` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `city_id` bigint unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `updated_at` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `version` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_idx_city_id` (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `wzz_crawler_log` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `crawler_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `request_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `response_body` text,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `wzz_seat` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `city_id` bigint unsigned NOT NULL DEFAULT '0',
  `store_id` bigint unsigned NOT NULL DEFAULT '0',
  `space_id` bigint unsigned NOT NULL DEFAULT '0',
  `seat_id` bigint unsigned NOT NULL DEFAULT '0',
  `space_name` varchar(255) NOT NULL,
  `coordinate_x` double NOT NULL DEFAULT '0',
  `coordinate_y` double NOT NULL DEFAULT '0',
  `status` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `version` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `wzz_store` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `city_id` bigint NOT NULL DEFAULT '0',
  `store_id` bigint unsigned NOT NULL DEFAULT '0',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `lon` double NOT NULL DEFAULT '0',
  `lat` double NOT NULL DEFAULT '0',
  `region` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `status` int NOT NULL DEFAULT '0',
  `seat_all` int unsigned NOT NULL DEFAULT '0',
  `seat_current_used` int unsigned NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `version` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_store_id` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `wzz_store_user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `city_id` bigint unsigned NOT NULL DEFAULT '0',
  `store_id` bigint unsigned NOT NULL DEFAULT '0',
  `user_id` bigint unsigned NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL,
  `version` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;