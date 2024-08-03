FactoryBot.define do
  factory :answer do
    sequence(:username, "user_1")
    sequence(:text, "Answer_1")
  end
end
