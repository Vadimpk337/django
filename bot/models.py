from django.db import models

import datetime

class User(models.Model):

	STATUS_CHOICES = [
	('A', 'Администратор'),
	('U', 'Пользователь'),
	('M', 'Модератор'),
	('B', 'Заблокированный')
	]
	first_name = models.CharField('Имя', max_length=64)
	telegram_id = models.IntegerField('Telegram ID', primary_key=True)
	status = models.CharField('Статус', max_length=1, choices=STATUS_CHOICES, default='U')

	def __str__(self):
		return f'Telegram ID: {self.telegram_id} | {self.status}: {self.first_name} '

	class Meta:

		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'


class Message(models.Model):

	telegram_id = models.IntegerField('Telegram ID')
	chat_id = models.IntegerField('ID чата')
	text = models.CharField('Сообщение', max_length=256)
	date = models.IntegerField('Время')

	def __str__(self):
		return f'{self.id} | \
		{datetime.datetime.utcfromtimestamp(self.date).strftime("%Y-%m-%d | %H:%M:%S")} | \
		{self.text} | {self.chat_id} | {self.telegram_id}'

	class Meta:

		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'




class Phone_operator(models.Model):

	title = models.CharField('Опетатор', max_length=64)
	code = models.CharField('Код', max_length=5, blank=False, primary_key=True)
	country = models.CharField('Страна', max_length=64)

	def __str__(self):
		return f'{self.code} | {self.title} {self.country}'

	class Meta:

		verbose_name = 'Оператор'
		verbose_name_plural = 'Операторы'


class Phone(models.Model):

	number = models.CharField('Номер', max_length=13, blank=False, primary_key=True)
	operator = models.ForeignKey(Phone_operator, on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.number}'

	class Meta:

		verbose_name = 'Номер'
		verbose_name_plural = 'Номера'
		

class Information(models.Model):

	phone = models.OneToOneField(Phone, on_delete=models.CASCADE, primary_key=True)

	IIN = models.CharField('ИИН', max_length=12, blank=True)

	bio = models.TextField('Биография', blank=True)

	first_name = models.CharField('Имя', max_length=64, blank=True)
	famaly_name = models.CharField('Фамилия', max_length=64, blank=True)
	last_name = models.CharField('Отчество', max_length=64, blank=True)

	email = models.CharField('Почта', max_length=64, blank=True)
	birthday = models.CharField('День рождения', max_length=10, blank=True)

	city = models.CharField('Город', max_length=64, blank=True)

	def __str__(self):
		return f'{self.phone} | {self.famaly_name} {self.first_name} {self.last_name}'

	class Meta:

		verbose_name = 'Информация о номере'
		verbose_name_plural = 'Информация о номерах'


class Comment(models.Model):

	user = models.ForeignKey(User, on_delete=models.PROTECT)

	description = models.TextField('Обращение', blank=True)
	date = models.IntegerField('Время')

	completed = models.BooleanField('Обработано', default=False)


	def __str__(self):
		return f'{self.completed} | {self.user} |{datetime.datetime.utcfromtimestamp(self.date).strftime("%Y-%m-%d | %H:%M:%S")} \
		| {self.description}'

	class Meta:

		verbose_name = 'Обращение'
		verbose_name_plural = 'Обращения'










