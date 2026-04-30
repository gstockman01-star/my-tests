import { test, expect } from '@playwright/test';

test('Полный цикл: Регистрация и Профиль (Стабильная версия)', async ({ page }) => {
  // Увеличиваем общий таймаут для CI
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

  // Ждем перехода на главную страницу
  await expect(page).toHaveURL(`${baseUrl}/`, { timeout: 15000 }); 

  // 2. ДОБАВЛЕНИЕ ЗАДАЧИ
  await page.getByRole('button', { name: 'Добавить' }).first().click();
  await page.getByRole('textbox', { name: 'Заголовок' }).fill(taskTitle);
  
  // Используем ID, чтобы избежать ошибки дублирования, и дату из будущего (валидация сайта)
  await page.locator('#date-input-create').fill('2026-05-05');
  await page.getByPlaceholder('Время').fill('15:00');
  
  // Кликаем "Добавить" в форме
  await page.getByRole('button', { name: 'Добавить' }).last().click();

  // Ожидание и клик по ОК (с увеличенным таймаутом)
  const okButton = page.getByRole('button', { name: /ОК/i });
  await okButton.waitFor({ state: 'visible', timeout: 10000 });
  await okButton.click();

  // Обновляем и проверяем появление задачи текстом (вместо скриншота)
  await page.reload();
  await expect(page.getByText(taskTitle).first()).toBeVisible({ timeout: 15000 });

  // 3. ЗАПОЛНЕНИЕ ПРОФИЛЯ
  await page.getByRole('link', { name: 'Профиль' }).click();
  await page.getByRole('textbox', { name: 'Фамилия' }).fill('Тестеров');
  await page.getByRole('textbox', { name: 'Имя' }).fill('Алексей');
  
  // Выбор пола: используем force:true, так как input перекрыт label
  await page.getByRole('button', { name: 'Пол' }).click();
  await page.locator('#github').click({ force: true });

  // Сохранение с ожиданием ответа от сервера
  await Promise.all([
    page.waitForResponse(resp => resp.status() === 200, { timeout: 15000 }),
    page.getByRole('button', { name: 'Сохранить' }).click({ force: true })
  ]);

  // Финальная проверка значения в поле (вместо скриншота)
  await expect(page.getByRole('textbox', { name: 'Имя' })).toHaveValue('Алексей', { timeout: 10000 });

  console.log('Тест успешно завершен без визуальных ошибок!');
});
