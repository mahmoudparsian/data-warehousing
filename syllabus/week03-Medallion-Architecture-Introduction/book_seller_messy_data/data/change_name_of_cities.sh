awk -F, 'BEGIN{OFS=","}
NR==1 {print; next}

{
    if ($10=="Australia" && $11=="CityA") $11="Sydney";
    else if ($10=="Australia" && $11=="CityB") $11="Melbourne";
    else if ($10=="Australia" && $11=="CityC") $11="Brisbane";
    else if ($10=="Australia" && $11=="CityD") $11="Perth";

    else if ($10=="Canada" && $11=="CityA") $11="Toronto";
    else if ($10=="Canada" && $11=="CityB") $11="Vancouver";
    else if ($10=="Canada" && $11=="CityC") $11="Montreal";
    else if ($10=="Canada" && $11=="CityD") $11="Calgary";

    else if ($10=="Germany" && $11=="CityA") $11="Berlin";
    else if ($10=="Germany" && $11=="CityB") $11="Munich";
    else if ($10=="Germany" && $11=="CityC") $11="Hamburg";
    else if ($10=="Germany" && $11=="CityD") $11="Frankfurt";

    else if ($10=="UK" && $11=="CityA") $11="London";
    else if ($10=="UK" && $11=="CityB") $11="Manchester";
    else if ($10=="UK" && $11=="CityC") $11="Birmingham";
    else if ($10=="UK" && $11=="CityD") $11="Leeds";

    else if ($10=="USA" && $11=="CityA") $11="New York";
    else if ($10=="USA" && $11=="CityB") $11="San Francisco";
    else if ($10=="USA" && $11=="CityC") $11="Chicago";
    else if ($10=="USA" && $11=="CityD") $11="Boston";

    print
}' sales.csv > sales_fixed.csv