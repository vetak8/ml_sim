SELECT
  age,
  income,
  dependents,
  has_property,
  has_car,
  credit_score,
  job_tenure,
  has_education,
  loan_amount,
  toDate(toUnixTimestamp(loan_deadline)) - toDate(toUnixTimestamp(loan_start)) as loan_period,
  if(
    toDate(toUnixTimestamp(loan_payed)) < toDate(toUnixTimestamp(loan_deadline)),
    0,
    toDate(toUnixTimestamp(loan_payed)) - toDate(toUnixTimestamp(loan_deadline))
  ) AS delay_days
FROM
  default.loan_delay_days
ORDER BY
  id