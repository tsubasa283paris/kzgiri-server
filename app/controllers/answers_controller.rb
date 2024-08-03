class AnswersController < ApplicationController
  before_action :set_answer, only: %i[update destroy]

  # POST /topics/:topic_id/answers
  def create
    @topic = Topic.find(params[:topic_id])
    @answer = @topic.answers.new(answer_params)

    if @answer.save
      render json: @answer
    else
      render json: @answer.errors, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /answers/1
  def update
    if @answer.update(answer_params)
      render json: @answer
    else
      render json: @answer.errors, status: :unprocessable_entity
    end
  end

  # DELETE /answers/1
  def destroy
    @answer.destroy!
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_answer
    @answer = Answer.find(params[:id])
  end

  # Only allow a list of trusted parameters through.
  def answer_params
    params.require(:answer).permit(:username, :text)
  end
end
