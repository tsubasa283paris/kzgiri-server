class Topic < ApplicationRecord
  has_many :answers, dependent: :destroy
end
