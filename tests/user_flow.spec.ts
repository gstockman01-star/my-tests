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

  // Проверка скриншота Dashboard
  const taskLocator = page.getByText(taskTitle).first();
  await expect(page).toHaveScreenshot('dashboard.png', { 
    mask: [taskLocator],
    animations: 'disabled'
  });

  // 3. ПРОФИЛЬ
  await page.getByRole('link', { name: 'Профиль' }).click();
  await page.getByRole('textbox', { name: 'Фамилия' }).fill('Тестеров');
  await page.getByRole('textbox', { name: 'Имя' }).fill('Алексей');
  
  // Выбор пола (исправлена опечатка в Myжской - латиница/кириллица)
  await page.getByRole('button', { name: 'Пол' }).click();
  await page.locator('text=/Мужской|Myжской/').last().click();

  await Promise.all([
    page.waitForResponse(resp => resp.status() === 200),
    page.getByRole('button', { name: 'Сохранить' }).click()
  ]);

  await page.waitForTimeout(1000);
  await expect(page).toHaveScreenshot('profile-page.png', { animations: 'disabled' });

  console.log('Тест завершен успешно!');
});
