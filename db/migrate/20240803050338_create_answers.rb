class CreateAnswers < ActiveRecord::Migration[7.1]
  def change
    create_table :answers do |t|
      t.string :username
      t.string :text
      t.references :topic, null: false, foreign_key: true

      t.timestamps
    end
  end
end
