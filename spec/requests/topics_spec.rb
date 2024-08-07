require "rails_helper"

RSpec.describe "/topics", type: :request do
  let(:valid_attributes) do
    { "text" => "valid text", "published_at" => 1.week.from_now.iso8601 }
  end

  let(:invalid_attributes) do
    {
      "text" => "too long text#{"-" * 300}",
      "published_at" => "string invalid as date"
    }
  end

  # This should return the minimal set of values that should be in the headers
  # in order to pass any filters (e.g. authentication) defined in
  # TopicsController, or in your router and rack
  # middleware. Be sure to keep this updated too.
  let(:valid_headers) { {} }

  # generate test data
  let(:topic) { FactoryBot.create(:topic) }

  describe ".index" do
    it "renders a successful response" do
      topic
      get topics_url, headers: valid_headers, as: :json
      expect(response).to be_successful
    end
  end

  describe ".show" do
    it "renders a successful response" do
      get topic_url(topic), as: :json
      expect(response).to be_successful
    end
  end

  describe ".create" do
    context "with valid parameters" do
      it "creates a new Topic" do
        expect {
          post topics_url,
               params: {
                 topic: valid_attributes
               },
               headers: valid_headers,
               as: :json
        }.to change(Topic, :count).by(1)
      end

      it "renders a JSON response with the new topic" do
        post topics_url,
             params: {
               topic: valid_attributes
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
          post topics_url, params: { topic: invalid_attributes }, as: :json
        }.to raise_error(ActiveRecord::ValueTooLong)
      end
    end
  end

  describe ".update" do
    context "with valid parameters" do
      let(:new_attributes) do
        { "text" => "updated text", "published_at" => 2.week.from_now.iso8601 }
      end

      it "renders a JSON response with the topic" do
        patch topic_url(topic),
              params: {
                topic: new_attributes
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
          patch topic_url(topic),
                params: {
                  topic: invalid_attributes
                },
                headers: valid_headers,
                as: :json
        }.to raise_error(ActiveRecord::ValueTooLong)
      end
    end
  end

  describe ".destroy" do
    it "destroys the requested topic" do
      topic
      expect {
        delete topic_url(topic), headers: valid_headers, as: :json
      }.to change(Topic, :count).by(-1)
    end
  end
end
