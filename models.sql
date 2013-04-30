BEGIN;
CREATE TABLE `books_publisher` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(30) NOT NULL,
    `address` varchar(50) NOT NULL,
    `city` varchar(60) NOT NULL,
    `state_province` varchar(30) NOT NULL,
    `country` varchar(50) NOT NULL,
    `website` varchar(200) NOT NULL
)
;
CREATE TABLE `books_author` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `email` varchar(75) NOT NULL
)
;
CREATE TABLE `books_book_authors` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `book_id` integer NOT NULL,
    `author_id` integer NOT NULL,
    UNIQUE (`book_id`, `author_id`)
)
;
ALTER TABLE `books_book_authors` ADD CONSTRAINT `author_id_refs_id_1a0a2829` FOREIGN KEY (`author_id`) REFERENCES `books_author` (`id`);
CREATE TABLE `books_book` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `isbn` varchar(20) NOT NULL,
    `title` varchar(100) NOT NULL,
    `publisher_id` integer NOT NULL,
    `publication_date` date NOT NULL
)
;
ALTER TABLE `books_book` ADD CONSTRAINT `publisher_id_refs_id_974c2a46` FOREIGN KEY (`publisher_id`) REFERENCES `books_publisher` (`id`);
ALTER TABLE `books_book_authors` ADD CONSTRAINT `book_id_refs_id_0a3634f3` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`);
CREATE TABLE `books_book_info` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `book_id` integer NOT NULL,
    `price` double precision NOT NULL,
    `numbers` integer NOT NULL
)
;
ALTER TABLE `books_book_info` ADD CONSTRAINT `book_id_refs_id_41c70fd3` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`);
CREATE TABLE `books_order_in` (
    `order_in_id` varchar(50) NOT NULL PRIMARY KEY,
    `order_date` date NOT NULL
)
;
CREATE TABLE `books_order_out` (
    `order_out_id` varchar(50) NOT NULL PRIMARY KEY,
    `order_date` date NOT NULL
)
;
CREATE TABLE `books_book_order_in` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `order_in_id_id` varchar(50) NOT NULL,
    `book_id_id` integer NOT NULL,
    `price` double precision NOT NULL,
    `numbers` integer UNSIGNED NOT NULL,
    `state` varchar(15) NOT NULL
)
;
ALTER TABLE `books_book_order_in` ADD CONSTRAINT `order_in_id_id_refs_order_in_id_1dabd0e1` FOREIGN KEY (`order_in_id_id`) REFERENCES `books_order_in` (`order_in_id`);
ALTER TABLE `books_book_order_in` ADD CONSTRAINT `book_id_id_refs_id_2af38745` FOREIGN KEY (`book_id_id`) REFERENCES `books_book` (`id`);
CREATE TABLE `books_book_order_out` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `order_out_id_id` varchar(50) NOT NULL,
    `book_id_id` integer NOT NULL,
    `numbers` integer UNSIGNED NOT NULL,
    `state` varchar(15) NOT NULL
)
;
ALTER TABLE `books_book_order_out` ADD CONSTRAINT `book_id_id_refs_id_fc65006d` FOREIGN KEY (`book_id_id`) REFERENCES `books_book` (`id`);
ALTER TABLE `books_book_order_out` ADD CONSTRAINT `order_out_id_id_refs_order_out_id_949531bf` FOREIGN KEY (`order_out_id_id`) REFERENCES `books_order_out` (`order_out_id`);
CREATE TABLE `books_record` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `order_in_id_id` varchar(50) NOT NULL,
    `order_out_id_id` varchar(50) NOT NULL,
    `order_tpye` varchar(5) NOT NULL,
    `money` double precision NOT NULL
)
;
ALTER TABLE `books_record` ADD CONSTRAINT `order_in_id_id_refs_order_in_id_5997c941` FOREIGN KEY (`order_in_id_id`) REFERENCES `books_order_in` (`order_in_id`);
ALTER TABLE `books_record` ADD CONSTRAINT `order_out_id_id_refs_order_out_id_7d35cca4` FOREIGN KEY (`order_out_id_id`) REFERENCES `books_order_out` (`order_out_id`);
CREATE INDEX `books_book_81b79144` ON `books_book` (`publisher_id`);
CREATE INDEX `books_book_info_36c249d7` ON `books_book_info` (`book_id`);
CREATE INDEX `books_book_order_in_c494a6b8` ON `books_book_order_in` (`order_in_id_id`);
CREATE INDEX `books_book_order_in_59f47779` ON `books_book_order_in` (`book_id_id`);
CREATE INDEX `books_book_order_out_81dbce4b` ON `books_book_order_out` (`order_out_id_id`);
CREATE INDEX `books_book_order_out_59f47779` ON `books_book_order_out` (`book_id_id`);
CREATE INDEX `books_record_c494a6b8` ON `books_record` (`order_in_id_id`);
CREATE INDEX `books_record_81dbce4b` ON `books_record` (`order_out_id_id`);

COMMIT;
