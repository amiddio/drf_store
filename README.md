# Internet Store

## Описание проекта

В этом проекте интернет магазина на DRF реализован следующий функционал:
* Токен авторизация пользователей
* Категории продуктов
* Продукты
* Можно ставить лайки и оценку (от 1 до 5) продуктам
* Возможность добавлять продукты в свой список желаний
* Корзина покупок
* Система скидочных купонов. В зависимости от типа купона скидка может быть фиксированной или процентной
* Оформление заказа

## На чем построен

Django, DRF, Djoser, unittests

## Список эндпойнтов

### Login

![Screenshot_1](/screenshots/endpoint_auth_token_login.png)

### Logout

![Screenshot_1](/screenshots/endpoint_auth_token_logout.png)

### Список категорий

Доступно для всех пользователей

![Screenshot_1](/screenshots/endpoint_get_categories.png)

### Категория

Доступно для всех пользователей

![Screenshot_1](/screenshots/endpoint_get_category_detail.png)

### Создание категории

Доступно только админам

![Screenshot_1](/screenshots/endpoint_post_categories.png)

### Изменение категории

Доступно только админам

![Screenshot_1](/screenshots/endpoint_patch_categories.png)

### Удаление категории

Доступно только админам

![Screenshot_1](/screenshots/endpoint_delete_categories.png)

### Список продуктов

Доступно для всех пользователей

![Screenshot_1](/screenshots/endpoint_get_products.png)

### Продукт

Доступно для всех пользователей

![Screenshot_1](/screenshots/endpoint_get_product_detail.png)

### Создание продукта

Доступно только админам

![Screenshot_1](/screenshots/endpoint_post_products.png)

### Изменение продукта

Доступно только админам

![Screenshot_1](/screenshots/endpoint_patch_products.png)

### Удаление продукта

Доступно только админам

![Screenshot_1](/screenshots/endpoint_delete_products.png)

### Установка like, wishlist, rate продуктам

![Screenshot_1](/screenshots/endpoint_product_relation.png)

### Wishlist

Список продуктов добавленных в wishlist. 
Доступно авторизованным пользователям. 

![Screenshot_1](/screenshots/endpoint_wishlist_products.png)

### Список продуктов в корзине

![Screenshot_1](/screenshots/endpoint_get_cart.png)

### Добавление продукта в корзину

![Screenshot_1](/screenshots/endpoint_post_cart.png)

### Изменение qty продукта в корзине

![Screenshot_1](/screenshots/endpoint_patch_cart.png)

### Удаление продукта из корзины

![Screenshot_1](/screenshots/endpoint_delete_cart.png)

### Применение купона в корзине

![Screenshot_1](/screenshots/endpoint_apply_coupon.png)
![Screenshot_1](/screenshots/endpoint_apply_coupon_cart.png)

### Удаление купона из корзины

![Screenshot_1](/screenshots/endpoint_delete_coupon_from_cart.png)

### Оформление заказа

![Screenshot_1](/screenshots/endpoint_order_create.png)
![Screenshot_1](/screenshots/endpoint_order_create_admin.png)
