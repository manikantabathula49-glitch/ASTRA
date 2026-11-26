# AI vs ML vs DL: shot list (80 clips, Chapters 2-7)

Every clip is 1080p30 MP4 in `out/`. The voiceover lines are suggestions: say them in your own
Telugu + English style. Trim or slow down clips in your editor to match your voice.


## Chapter 2: The Big Picture

| # | File | Length | Suggested voiceover |
|---|---|---|---|
| 1 | `C01_chapter2_card.mp4` | 6s | Chapter 2. First, let's see the big picture: how AI, ML and DL are connected. |
| 2 | `C02_ai_ml_dl_circles.mp4` | 13s | Think of three circles. AI is the biggest. Machine Learning is inside AI. Deep Learning is inside Machine Learning. |
| 3 | `C03_define_ai.mp4` | 8s | AI means making machines do tasks that normally need human intelligence. |
| 4 | `C04_define_ml.mp4` | 8s | Machine Learning is a part of AI where the machine learns from data instead of fixed rules. |
| 5 | `C05_define_dl.mp4` | 8s | Deep Learning is a part of ML that uses neural networks with many layers. |
| 6 | `C06_history_timeline.mp4` | 12s | AI started in the 1950s. ML came next. Deep Learning exploded after 2012, and ChatGPT arrived in 2022. |
| 7 | `C07_rules_vs_learning.mp4` | 18s | In normal programming, we give rules and data to get answers. In ML, we give data and answers, and the machine finds the rules. |
| 8 | `C08_rule_ai_vs_ml.mp4` | 9s | Rule-based AI only follows the rules we write. ML learns from examples, so it can handle new cases. |
| 9 | `C09_ai_without_ml.mp4` | 10s | Not every AI learns. GPS route finding and old chess programs are AI, but not Machine Learning. |
| 10 | `C10_sort_examples.mp4` | 18s | Let's sort some examples into AI, ML and DL. |
| 11 | `C11_quiz_chatgpt.mp4` | 12s | Quick quiz! ChatGPT belongs to which field? Pause and think. |

## Chapter 3: How ML Learns

| # | File | Length | Suggested voiceover |
|---|---|---|---|
| 12 | `C12_chapter3_card.mp4` | 6s | Chapter 3. Now the most important part: how does a machine actually learn? |
| 13 | `C13_student_analogy.mp4` | 11s | ML is just like a student. Practice questions are training data, and the final exam is test data. |
| 14 | `C14_dataset_table.mp4` | 15s | Here is a dataset of houses. Size, bedrooms and location are features. Price is the label we want to predict. |
| 15 | `C15_define_features_label.mp4` | 8s | Features are the inputs. The label is the answer. |
| 16 | `C16_ml_pipeline.mp4` | 15s | Every ML project follows these steps: collect data, clean it, choose a model, train, test and use it. |
| 17 | `C17_train_test_split.mp4` | 11s | We split the data: 80% to train the model, and 20% kept hidden to test it, like a final exam. |
| 18 | `C18_regression_fit.mp4` | 13s | The model starts with a bad line. Training moves the line until the total error is the smallest. |
| 19 | `C19_define_loss.mp4` | 7s | Loss is a number that shows how wrong the model is. Training tries to make it as small as possible. |
| 20 | `C20_gradient_descent.mp4` | 13s | Gradient descent is like walking downhill in fog. Each step goes towards lower error, until we reach the bottom. |
| 21 | `C21_loss_curve.mp4` | 9s | As training goes on, the loss goes down and the accuracy goes up. |
| 22 | `C22_training_loop.mp4` | 14s | Training is a loop: predict, measure the error, adjust, and repeat thousands of times. |
| 23 | `C23_overfitting_plots.mp4` | 11s | Underfit is too simple. Overfit memorizes the noise. We want a good fit in the middle. |
| 24 | `C24_under_vs_overfit.mp4` | 10s | Underfitting is like not studying. Overfitting is like memorizing answers without understanding. |
| 25 | `C25_what_is_model.mp4` | 8s | A model is simply a maths function. Training finds the best numbers inside it. |
| 26 | `C26_spam_example.mp4` | 12s | When a new email arrives, the trained model checks the patterns and says: spam, 98% sure. |
| 27 | `C27_quiz_label.mp4` | 12s | Quiz time! What is a label? |

## Chapter 4: Types of ML

| # | File | Length | Suggested voiceover |
|---|---|---|---|
| 28 | `C28_chapter4_card.mp4` | 6s | Chapter 4. Machine Learning has three main types. |
| 29 | `C29_three_types.mp4` | 7s | Supervised learns with answers, unsupervised finds patterns alone, and reinforcement learns from rewards. |
| 30 | `C30_define_supervised.mp4` | 8s | Supervised learning means learning with a teacher. Every example has the correct answer. |
| 31 | `C31_classification.mp4` | 10s | Classification draws a boundary. For a new student, the model checks which side they fall on. |
| 32 | `C32_class_vs_regression.mp4` | 11s | Classification gives a category. Regression gives a number. |
| 33 | `C33_define_unsupervised.mp4` | 8s | Unsupervised learning has no answers. The model finds the groups by itself. |
| 34 | `C34_clustering.mp4` | 13s | K-Means places centres, groups nearby points, moves the centres, and repeats until the groups are clear. |
| 35 | `C35_unsupervised_uses.mp4` | 8s | Unsupervised learning is used for customer groups, fraud detection and recommendations. |
| 36 | `C36_define_rl.mp4` | 8s | Reinforcement learning is learning by trial and error, with rewards and penalties. |
| 37 | `C37_rl_grid.mp4` | 12s | The robot falls into a trap first and gets minus ten. Next time it finds the goal and gets plus ten. |
| 38 | `C38_rl_loop.mp4` | 14s | The agent takes an action, the environment gives a reward, and the loop repeats. |
| 39 | `C39_types_table.mp4` | 8s | Here's the summary of all three types. Screenshot this for your exams! |
| 40 | `C40_sort_types.mp4` | 17s | Let's sort these examples into the three types. |
| 41 | `C41_quiz_unsupervised.mp4` | 12s | Quiz! Grouping customers without labels is which type? |

## Chapter 5: ML Algorithms

| # | File | Length | Suggested voiceover |
|---|---|---|---|
| 42 | `C42_chapter5_card.mp4` | 6s | Chapter 5. Let's meet the most popular ML algorithms. |
| 43 | `C43_define_linear_regression.mp4` | 8s | Linear regression predicts a number by drawing the best straight line. |
| 44 | `C44_logistic_sigmoid.mp4` | 11s | Logistic regression gives a probability between zero and one. Above 0.5 we say spam. |
| 45 | `C45_decision_tree.mp4` | 13s | A decision tree asks yes or no questions, step by step, until it reaches an answer. |
| 46 | `C46_random_forest.mp4` | 10s | Random forest builds many trees and lets them vote. The majority wins. |
| 47 | `C47_knn.mp4` | 11s | KNN looks at the nearest neighbours. Three are cats and two are dogs, so it predicts cat. |
| 48 | `C48_define_kmeans.mp4` | 8s | K-Means splits data into K groups. You choose K. |
| 49 | `C49_define_svm.mp4` | 8s | SVM draws the boundary with the widest gap between the classes. |
| 50 | `C50_algorithms_table.mp4` | 14s | Here's your algorithm cheat sheet. Save it for revision. |
| 51 | `C51_quiz_regression.mp4` | 12s | Quiz! Which algorithm predicts a number? |

## Chapter 6: Deep Learning

| # | File | Length | Suggested voiceover |
|---|---|---|---|
| 52 | `C52_chapter6_card.mp4` | 6s | Chapter 6. Now, Deep Learning: the technology behind ChatGPT. |
| 53 | `C53_brain_vs_artificial.mp4` | 12s | An artificial neuron is inspired by brain neurons, but it's much simpler. |
| 54 | `C54_neuron.mp4` | 12s | Each input is multiplied by a weight, added up, passed through an activation, and sent forward. |
| 55 | `C55_activation_functions.mp4` | 10s | Activation functions add curves. ReLU is used in hidden layers, sigmoid gives probabilities. |
| 56 | `C56_neural_network.mp4` | 13s | Connect many neurons in layers and you get a neural network. Many hidden layers means deep learning. |
| 57 | `C57_define_deep.mp4` | 7s | Why is it called deep? Because it has many hidden layers. |
| 58 | `C58_backprop.mp4` | 14s | The network makes a wrong guess, sends the error backward, fixes its weights, and gets it right. |
| 59 | `C59_feature_engineering.mp4` | 14s | In ML, humans pick the features. In DL, the network learns the features by itself. |
| 60 | `C60_feature_hierarchy.mp4` | 12s | Early layers find edges, then shapes, then parts like eyes, and finally a whole face. |
| 61 | `C61_cnn_filter.mp4` | 12s | A CNN slides small filters over the image to detect patterns like edges. |
| 62 | `C62_network_types.mp4` | 8s | Different networks for different jobs: CNNs for images, Transformers for language. |
| 63 | `C63_llm_next_word.mp4` | 12s | LLMs like ChatGPT predict the next word. Attention decides which words matter most. |
| 64 | `C64_data_vs_performance.mp4` | 10s | With small data, traditional ML wins. With big data, deep learning keeps getting better. |
| 65 | `C65_dl_needs.mp4` | 8s | Deep learning needs huge data, powerful GPUs and a lot of training time. |
| 66 | `C66_cpu_vs_gpu.mp4` | 9s | A CPU has a few strong cores. A GPU has thousands of small cores, perfect for neural networks. |
| 67 | `C67_dl_around_you.mp4` | 11s | You use deep learning every day: face unlock, Google Translate, ChatGPT. |
| 68 | `C68_dl_limits.mp4` | 8s | But deep learning has limits: it's a black box, data hungry, and can be confidently wrong. |
| 69 | `C69_quiz_deep.mp4` | 12s | Quiz! Why is deep learning called deep? |

## Chapter 7: Final Revision

| # | File | Length | Suggested voiceover |
|---|---|---|---|
| 70 | `C70_chapter7_card.mp4` | 6s | Chapter 7. Let's put everything together for your exams. |
| 71 | `C71_final_table_1.mp4` | 11s | Here is the full comparison. Pause and screenshot this one. |
| 72 | `C72_final_table_2.mp4` | 11s | And here is ML versus DL, the most common exam question. |
| 73 | `C73_self_driving_levels.mp4` | 7s | One self-driving car uses all three: AI for decisions, ML for patterns, DL for vision. |
| 74 | `C74_exam_definitions.mp4` | 8s | For 2-mark questions, write these one-line definitions. |
| 75 | `C75_exam_differences.mp4` | 10s | For long answers, remember these five differences. |
| 76 | `C76_quiz_most_data.mp4` | 12s | Final quiz round! Which needs the most data? |
| 77 | `C77_quiz_netflix.mp4` | 12s | Netflix recommendations: which one is it? |
| 78 | `C78_quiz_robot.mp4` | 12s | Last one: a robot learning to walk with rewards? |
| 79 | `C79_recap_circles.mp4` | 13s | So remember: AI is the big circle, ML is inside it, and DL is inside ML. |
| 80 | `C80_outro.mp4` | 9s | If this helped, subscribe to AI with Mani and share it with your friends preparing for exams. |

**Total animation time: 14.1 minutes**
