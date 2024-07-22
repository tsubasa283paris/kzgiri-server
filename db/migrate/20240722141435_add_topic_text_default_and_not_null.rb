class AddTopicTextDefaultAndNotNull < ActiveRecord::Migration[7.1]
  def change
    change_column_default :topics, :text, ''
    change_column_null :topics, :text, false
  end
end
