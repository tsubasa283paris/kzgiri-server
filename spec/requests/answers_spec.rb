require "rails_helper"

RSpec.describe "/topics/:topic_id/answers", type: :request do
  let(:valid_attributes) do
    { "username" => "valid username", "text" => "valid text" }
  end

  let(:invalid_attributes) do
    {
      "username" => "too long username#{"-" * 100}",
      "text" => "too long text#{"-" * 300}"
    }
  end

  # This should return the minimal set of values that should be in the headers
  # in order to pass any filters (e.g. authentication) defined in
  # AnswersController, or in your router and rack
  # middleware. Be sure to keep this updated too.
  let(:valid_headers) { {} }

  # generate test data
  let(:topic) { FactoryBot.create(:topic) }
  let(:answer) { FactoryBot.create(:answer) }

  describe ".create" do
    context "with valid parameters" do
      it "creates a new Answer" do
        expect {
          post topic_answers_url(topic),
               params: {
                 answer: valid_attributes
               },
               headers: valid_headers,
               as: :json
        }.to change(Answer, :count).by(1)
      end

      it "renders a JSON response with the new answer" do
        post topic_answers_url(topic),
             params: {
               answer: valid_attributes
             },
             headers: valid_headers,
             as: :json
        expect(response).to have_http_status(:ok)
        expect(response.content_type).to match(
          a_string_including("application/json")
        )
      end
    end

    context "with invalid parameters" do
      it "does raise ActiveRecord::ValueTooLong" do
        expect {
          post topic_answers_url(topic),
               params: {
                 answer: invalid_attributes
               },
               as: :json
        }.to raise_error(ActiveRecord::ValueTooLong)
      end
    end
  end

  describe ".update" do
    context "with valid parameters" do
      let(:new_attributes) do
        { "username" => "updated username", "text" => "updated text" }
      end

      it "renders a JSON response with the answer" do
        patch topic_answer_url(topic, answer),
              params: {
                answer: new_attributes
              },
              headers: valid_headers,
              as: :json
        expect(response).to have_http_status(:ok)
        expect(response.content_type).to match(
          a_string_including("application/json")
        )
      end
    end

    context "with invalid parameters" do
      it "does raise ActiveRecord::ValueTooLong" do
        expect {
          patch topic_answer_url(topic, answer),
                params: {
                  answer: invalid_attributes
                },
                headers: valid_headers,
                as: :json
        }.to raise_error(ActiveRecord::ValueTooLong)
      end
    end
  end

  describe ".destroy" do
    it "destroys the requested answer" do
      topic
      answer
      expect {
        delete topic_answer_url(topic, answer),
               headers: valid_headers,
               as: :json
      }.to change(Answer, :count).by(-1)
    end
  end
end
