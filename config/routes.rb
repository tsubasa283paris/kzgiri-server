Rails.application.routes.draw do
  resources :topics do
    resources :answers, except: %i[index show]
  end
end
