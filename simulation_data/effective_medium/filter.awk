BEGIN {
}
/Parameters/ {
    match($0, /np_size=([0-9]*.[0-9]*)/, a);
    np_size = a[1]
    match($0, /sigb=([0-9]*)/, a);
    sigb = a[1]
}

{
    match(FILENAME, /(param_sweep.*)\.txt/, a);
    fname = a[1]
    print $0  >> (fname "_" np_size "_" sigb ".txt")
}

