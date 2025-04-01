import random
import os


def load_questions(filename):
    result = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                q, a, d = line.split('|')
                result.append({
                    'question': q.strip(),
                    'answer': [ans.strip().lower() for ans in a.split('/')],
                    'difficulty': d.strip()
                })
    return result


def ask_question(round_number, question):
    print(f"\nРаунд {round_number}")
    print(f"Вопрос: {question['question']}")
    return input("Ваш ответ (или введите 'выход' для завершения игры): ").strip().lower()


def save_result(player_name, player_score, viewers_score):
    results_file = "game_results.txt"
    if player_score > viewers_score:
        wins, losses = (1, 0)
    else:
        wins, losses = (0, 1)

    results_dict = {}

    if os.path.exists(results_file):
        with open(results_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            name, record = line.strip().split(': ')
            existing_wins, existing_losses = map(int, record.split(' - '))
            results_dict[name] = (existing_wins, existing_losses)

        if player_name in results_dict:
            action = input(
                f"Имя '{player_name}' уже существует. Вы хотите объединить результаты (введите '1') или сохранить под новым именем (введите '2')? ").strip()
            if action == '1':
                wins += results_dict[player_name][0]
                losses += results_dict[player_name][1]
            else:
                suffix = 1
                new_name = f"{player_name}_{suffix}"
                while new_name in results_dict:
                    suffix += 1
                    new_name = f"{player_name}_{suffix}"
                player_name = new_name

        results_dict[player_name] = (wins, losses)

    else:
        results_dict[player_name] = (wins, losses)

    sorted_results = []
    for name, (player_wins, player_losses) in results_dict.items():
        sorted_results.append((name, player_wins, player_losses))
    sorted_results.sort(key=lambda x: x[1], reverse=True)

    with open(results_file, 'w', encoding='utf-8') as f:
        for name, player_wins, player_losses in sorted_results:
            f.write(f"{name}: {player_wins} - {player_losses}\n")


def display_top_results():
    results_file = "game_results_var2.txt"
    if not os.path.exists(results_file):
        print("Результаты игр пока отсутствуют.")
        return

    print("\nТоп результатов игр:")
    with open(results_file, 'r', encoding='utf-8') as f:
        results = []
        for line in f.readlines():
            results.append(line.strip())

    results.sort(key=lambda x: int(x.split(': ')[1].split(' - ')[0]), reverse=True)
    for idx, result in enumerate(results[:10], 1):
        print(f"{idx}. {result}")


def filter_questions_by_difficulty(questions, difficulty):
    filtered_questions = []
    for q in questions:
        if q['difficulty'] == difficulty:
            filtered_questions.append(q)
    return filtered_questions


def main():
    questions_file = "questions.txt"
    questions = load_questions(questions_file)

    print("Выберите уровень сложности: легкий, средний, сложный")
    difficulty = input("Введите сложность: ").strip().lower()

    if difficulty not in ['легкий', 'средний', 'сложный']:
        print("Неверный выбор. Устанавливается уровень сложности по умолчанию: средний.")
        difficulty = 'средний'

    questions = filter_questions_by_difficulty(questions, difficulty)
    random.shuffle(questions)

    player_score = 0
    viewers_score = 0
    round_number = 1

    asked_questions = []

    print("Добро пожаловать в игру \"Что? Где? Когда?\"!")
    print("Игра идет до 6 очков одной из сторон. Удачи!\n")

    while player_score < 6 and viewers_score < 6:
        if not questions:
            print("Вопросы закончились! Игра завершена.")
            break

        question = questions.pop()
        asked_questions.append(question)

        player_answer = ask_question(round_number, question)

        if player_answer == 'выход':
            print("Игра завершена досрочно. Спасибо за участие!")
            break

        if player_answer in question['answer']:
            print("Правильно! Вы зарабатываете 1 очко.")
            player_score += 1
        else:
            print(f"Неправильно. Правильный ответ: {', '.join(question['answer'])}.")
            viewers_score += 1

        print(f"Счет: Игрок - {player_score}, Команда телезрителей - {viewers_score}\n")
        round_number += 1

    if player_score >= 6:
        print("Поздравляем! Вы победили в этой игре.")
    elif viewers_score >= 6:
        print("К сожалению, победила команда телезрителей. Удачи в следующей игре!")

    print(f"Итоговый счет: Игрок - {player_score}, Команда телезрителей - {viewers_score}")

    save_game = input("Вы хотите сохранить результат игры? (да/нет): ").strip().lower()
    if save_game == 'да':
        player_name = input("Введите ваше имя: ").strip()
        save_result(player_name, player_score, viewers_score)
        print(f"Ваш счет: {player_name} {player_score}: {viewers_score}")

    display_top_results()


main()
