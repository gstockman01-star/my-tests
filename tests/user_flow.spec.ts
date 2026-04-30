import { test, expect } from '@playwright/test';

test('Полный цикл: Регистрация, Профиль и Проверка всего UI', async ({ page }) => {
  // Увеличиваем таймаут для стабильности вheaded режиме
  test.setTimeout(120000);

  const baseUrl = 'http://2.59.41.2:6700';
  const uniqueId = Date.now();
  const email = `user${uniqueId}@test.ru`;
  const pass = 'proba4@mail.ru';
  const taskTitle = `Задача ${uniqueId}`;

  // --- 1. РЕГИСТРАЦИЯ ---
  await page.goto(`${baseUrl}/auth/register`);
  await expect(page.getByRole('heading', { name: /Регистрация/i })).toBeVisible();
  
  await page.getByPlaceholder('почта').fill(email);
  await page.getByPlaceholder('пароль', { exact: true }).fill(pass);
  await page.getByPlaceholder('повторите пароль').fill(pass);
  await page.getByRole('button', { name: 'Зарегистрироваться' }).click();

  await expect(page).toHaveURL(`${baseUrl}/`, { timeout: 15000 }); 

  // --- 2. ДОБАВЛЕНИЕ ЗАДАЧИ ---
  await page.getByRole('button', { name: 'Добавить' }).first().click();
  await page.getByRole('textbox', { name: 'Заголовок' }).fill(taskTitle);
  
  // Актуальная дата (сегодня)
  const today = new Date().toLocaleDateString('en-CA'); 
  await page.getByPlaceholder('Дата').fill(today);
  await page.getByPlaceholder('Время').fill('15:00');
  
  await page.getByRole('button', { name: 'Добавить' }).last().click();

  const okButton = page.getByRole('button', { name: /ОК/i });
  await okButton.waitFor({ state: 'visible' });
  await okButton.click();

  // Обновляем страницу, чтобы задача точно появилась в DOM
  await page.reload();
  const taskLocator = page.getByText(taskTitle).first();
  await taskLocator.waitFor({ state: 'visible', timeout: 15000 });

  // Скриншот Dashboard с допуском по пикселям
  await expect(page).toHaveScreenshot('dashboard.png', { 
    mask: [taskLocator],
    maxDiffPixelRatio: 0.05,
    caret: 'hide',
    animations: 'disabled'
  });

  // --- 3. ЗАПОЛНЕНИЕ ПРОФИЛЯ ---
  await page.getByRole('link', { name: 'Профиль' }).click();
  
  // Проверка навигации (только первый элемент nav)
  await expect(page.locator('nav').first()).toHaveScreenshot('header-profile.png', {
    maxDiffPixelRatio: 0.05,
    animations: 'disabled'
  });
  
  await page.getByRole('textbox', { name: 'Фамилия' }).fill('Тестеров');
  await page.getByRole('textbox', { name: 'Имя' }).fill('Алексей');
  await page.getByRole('textbox', { name: 'Отчество' }).fill('Иванович');
  
  // Дата рождения
  const bDay = page.getByRole('textbox', { name: 'Дата рождения' });
  await bDay.click();
  await bDay.fill('2000-12-12');

  // ПОЛ (Выпадающий список)
  await page.getByRole('button', { name: 'Пол' }).click({ force: true });
  await page.locator('text=Myжской').last().click({ force: true });

  // ТЕЛЕФОН (Имитация клавиатуры для маски)
  const phoneInput = page.locator('input[placeholder="Телефон"]');
  await phoneInput.click({ force: true });
  await page.keyboard.type('9262346578', { delay: 50 });
  
  // Сохранение с ожиданием ответа от API
  await Promise.all([
    page.waitForResponse(resp => resp.status() === 200, { timeout: 15000 }),
    page.getByRole('button', { name: 'Сохранить' }).click({ force: true })
  ]);

  // Ждем отрисовку финального состояния профиля
  await page.waitForTimeout(2000); 
  await expect(page).toHaveScreenshot('profile-page.png', {
    maxDiffPixelRatio: 0.05,
    caret: 'hide',
    animations: 'disabled'
  });

  // --- 4. ПЕРЕЗАХОД ---
  await page.getByText('Выйти').click();
  
  await page.getByPlaceholder('почта').fill(email);
  await page.locator('input[type="password"]').fill(pass);
  await page.getByRole('button', { name: 'Войти' }).click();

  // --- 5. ИТОГОВАЯ ПРОВЕРКА ---
  await expect(page.getByText(taskTitle).first()).toBeVisible({ timeout: 15000 });
  
  await page.getByRole('link', { name: 'Профиль' }).click();
  const finalNameInput = page.getByRole('textbox', { name: 'Имя' });
  await expect(finalNameInput).toHaveValue('Алексей', { timeout: 10000 });

  console.log('Тест успешно завершен!');
});
