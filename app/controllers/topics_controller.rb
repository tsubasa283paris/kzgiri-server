class TopicsController < ApplicationController
  before_action :set_topic, only: %i[show update destroy]

  # GET /topics
  def index
    @topics = Topic.all

    render json: @topics, each_serializer: TopicsSerializer
  end

  # GET /topics/:id
  def show
    render json: @topic, serializer: DetailedTopicsSerializer
  end

  # POST /topics
  def create
    return @response unless post_params_is_valid?

    @topic = Topic.new(post_params)

    if @topic.save
      render json: @topic, serializer: DetailedTopicsSerializer
    else
      render json: @topic.errors, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /topics/:id
  def update
    return @response unless post_params_is_valid?

    if @topic.update(post_params)
      render json: @topic, serializer: DetailedTopicsSerializer
    else
      render json: @topic.errors, status: :unprocessable_entity
    end
  end

  # DELETE /topics/:id
  def destroy
    @topic.destroy!
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_topic
    @topic = Topic.find(params[:id])
  end

  def post_params
    params.require(:topic).permit(:text, :published_at)
  end

  # Validates parameters for create and update.
  def post_params_is_valid?
    # filter keys
    begin
      # return 400 to published_at that is not future-like
      if Time.iso8601(post_params[:published_at]) <= 1.minute.after(Time.now)
        @response =
          render json: {
                   "error" =>
                     "Parameter 'published_at' must not be a past time."
                 },
                 status: :bad_request
        return false
      end
    rescue ArgumentError
      # return 400 when published_at is not a valid ISO string
      @response =
        render json: {
                 "error" =>
                   "Parameter 'published_at' must be a valid ISO formatted datetime string."
               },
               status: :bad_request
      return false
    end
    true
  end
end
