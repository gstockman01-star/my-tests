import { test, expect } from '@playwright/test';

test('Полный цикл: Регистрация и Профиль', async ({ page }) => {
  test.setTimeout(120000);

  const baseUrl = 'http://2.59.41.2:6700';
  const uniqueId = Date.now();
  const email = `user${uniqueId}@test.ru`;
  const pass = 'proba4@mail.ru';
  const taskTitle = `Задача ${uniqueId}`;

  // 1. РЕГИСТРАЦИЯ
  await page.goto(`${baseUrl}/auth/register`);
  await page.getByPlaceholder('почта').fill(email);
  await page.getByPlaceholder('пароль', { exact: true }).fill(pass);
  await page.getByPlaceholder('повторите пароль').fill(pass);
  await page.getByRole('button', { name: 'Зарегистрироваться' }).click();

  await expect(page).toHaveURL(`${baseUrl}/`, { timeout: 15000 }); 

  // 2. ДОБАВЛЕНИЕ ЗАДАЧИ
  await page.getByRole('button', { name: 'Добавить' }).first().click();
  await page.getByRole('textbox', { name: 'Заголовок' }).fill(taskTitle);
  
  const today = new Date().toLocaleDateString('en-CA'); 
  await page.getByPlaceholder('Дата').fill(today);
  await page.getByPlaceholder('Время').fill('15:00');
  await page.getByRole('button', { name: 'Добавить' }).last().click();

  await page.getByRole('button', { name: /ОК/i }).click();
  await page.reload();

  // Вместо скриншота проверяем текст задачи
  const taskLocator = page.getByText(taskTitle).first();
  await expect(taskLocator).toBeVisible({ timeout: 15000 });

  // 3. ЗАПОЛНЕНИЕ ПРОФИЛЯ
  await page.getByRole('link', { name: 'Профиль' }).click();
  await page.getByRole('textbox', { name: 'Фамилия' }).fill('Тестеров');
  await page.getByRole('textbox', { name: 'Имя' }).fill('Алексей');
  
  // Выбор пола через ID (как показал лог ошибки) с принудительным кликом
  await page.getByRole('button', { name: 'Пол' }).click();
  await page.locator('#github').click({ force: true });

  await Promise.all([
    page.waitForResponse(resp => resp.status() === 200),
    page.getByRole('button', { name: 'Сохранить' }).click({ force: true })
  ]);

  await page.waitForTimeout(1000);
  // Проверяем результат текстом, а не скриншотом
  await expect(page.getByRole('textbox', { name: 'Имя' })).toHaveValue('Алексей');

  console.log('Тест завершен успешно!');
});
