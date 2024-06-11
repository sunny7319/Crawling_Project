import argparse



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--predata', default=1, type=int)
    parser.add_argument('--premodel', default=0, type=int)
    parser.add_argument('--allpreprocess', default=0, type=int)
    parser.add_argument('--model_vec_size', default=16, type=int)
    parser.add_argument('--model_win_size', default=3, type=int)
    parser.add_argument('--model_neg_size', default=5, type=int)
    parser.add_argument('--model_min_size', default=4, type=int)
    parser.add_argument('--search_name',default='한화비전', type=str)
    parser.add_argument('--search_skill',action='store', nargs='*',default=['AWS','MySQL'],type=str,help="Examples: -i item1 item2, -i item3")
    parser.add_argument('--prompt_mode',default=1, type=int)
    args = parser.parse_args()
    return args