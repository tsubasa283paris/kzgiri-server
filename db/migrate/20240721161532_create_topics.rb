class CreateTopics < ActiveRecord::Migration[7.1]
  def change
    create_table :topics do |t|
      t.string :text
      t.datetime :published_at

      t.timestamps
    end
  end
end
