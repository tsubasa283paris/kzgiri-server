FactoryBot.define do
  factory :topic do
    sequence(:text, "Topic_1")
    published_at { 1.week.from_now.iso8601 }
  end
end
