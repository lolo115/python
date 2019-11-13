import argparse as arg
import json

""" Documentation https://docs.python.org/fr/3.5/howto/argparse.html """

if __name__=='__main__':
    parser=arg.ArgumentParser()
    parser.add_argument("-a1","--argument1", help="Ceci est le premier argument typé entier", type=int)
    parser.add_argument("-a2", help="Ceci est le second argument typé entier, en mode TRUE/FALSE", action="store_true")
    parser.add_argument("-a3", help="Ceci est le troisième argument de type entier sous liste contrainte de valeur", type=int, choices=[1,2,3,4])
    parser.add_argument("-a4", help="Quatrieme argument", choices=["a","b","c"])
    parser.add_argument("-a5", help="Cinquieme argument", nargs='*', choices=["a", "b", "c"])
    args=parser.parse_args()
    if args.argument1:
        print("Argument1 on")
        print("  Value = ", args.argument1)
    if args.a2:
        print("Argument2 (a2) on")
        print("  Value = ",args.a2)
    if args.a3:
        print("Argument3 (a3) on")
        print("  Value = ",args.a3)
    if args.a4:
        print("Argument4 (a4) on")
        print("  Value = ",args.a4)
    if args.a5:
        print("Argument5 (a5) on")
        for p in args.a5:
            print("  Values = ",p)

    print("Liste complete: ")
    print("\n".join("{}\t\t{}".format(k, v) for k, v in vars(args).items()))

    print("Liste complete (JSON)")
    print(json.dumps(vars(args), indent=4, sort_keys=False))
