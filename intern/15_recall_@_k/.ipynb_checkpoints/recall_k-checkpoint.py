from typing import List


def recall_at_k(labels: List[int], scores: List[float], k=5) -> float:
    # Сортируем по убыванию по предсказанным оценкам
    sorted_indices = sorted(range(len(scores)), key=lambda x: scores[x], reverse=True)

    # Выбираем топ-K элементов
    top_k_predictions = [labels[i] for i in sorted_indices[:k]]

    # Подсчитываем количество релевантных элементов в топ-K
    relevant_in_top_k = sum(top_k_predictions)

    # Подсчитываем общее количество релевантных элементов
    total_relevant = sum(labels)

    # Вычисляем Recall @ K
    recall_k = relevant_in_top_k / total_relevant if total_relevant > 0 else 0.0

    return recall_k


def precision_at_k(labels: List[int], scores: List[float], k=5) -> float:
    # Сортируем по убыванию по предсказанным оценкам
    sorted_indices = sorted(range(len(scores)), key=lambda x: scores[x], reverse=True)

    # Выбираем топ-K элементов
    top_k_predictions = [labels[i] for i in sorted_indices[:k]]

    # Подсчитываем количество релевантных элементов в топ-K
    relevant_in_top_k = sum(top_k_predictions)

    # Вычисляем Precision @ K
    precision_k = relevant_in_top_k / k if k > 0 else 0.0

    return precision_k


def specificity_at_k(labels: List[int], scores: List[float], k=5) -> float:
    # Сортируем по убыванию по предсказанным оценкам
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)


    # Подсчитываем количество нерелевантных элементов вне топ-K
    non_relevant_outside_top_k = len([label for i, label in enumerate(labels) if label == 0 and i not in sorted_indices[:k]])

    # Подсчитываем общее количество нерелевантных элементов
    total_non_relevant = len([label for label in labels if label == 0])

    # Вычисляем Specificity @ K
    specificity_at_k = non_relevant_outside_top_k / total_non_relevant if total_non_relevant > 0 else 0.0

    return specificity_at_k

def f1_at_k(labels: List[int], scores: List[float], k=5) -> float:
    # Вычисляем Recall и Precision @ K
    recall = recall_at_k(labels, scores, k)
    precision = precision_at_k(labels, scores, k)

    # Recall + Precision
    rp =  recall + precision

    # Вычисляем F1-Score @ K
    f1_score_at_k = (2 * recall * precision) / rp if rp > 0 else 0.0

    return f1_score_at_k
