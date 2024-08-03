Rails.application.routes.draw do
  resources :topics do
    resources :answers
  end
end
