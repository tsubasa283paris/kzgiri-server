require "rails_helper"

RSpec.describe AnswersController, type: :routing do
  describe "routing" do
    it "routes to #create" do
      expect(post: "/topics/1/answers").to route_to(
        "answers#create",
        topic_id: "1"
      )
    end

    it "routes to #update via PUT" do
      expect(put: "/topics/1/answers/1").to route_to(
        "answers#update",
        topic_id: "1",
        id: "1"
      )
    end

    it "routes to #update via PATCH" do
      expect(patch: "/topics/1/answers/1").to route_to(
        "answers#update",
        topic_id: "1",
        id: "1"
      )
    end

    it "routes to #destroy" do
      expect(delete: "/topics/1/answers/1").to route_to(
        "answers#destroy",
        topic_id: "1",
        id: "1"
      )
    end
  end
end
