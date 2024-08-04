class TopicsSerializer < ActiveModel::Serializer
  attributes :id, :created_at, :published_at, :text, :answers
end
