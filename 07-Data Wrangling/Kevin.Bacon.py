import pandas as pd

# Read in the airports data.
airports = pd.read_csv("data/airports.dat", header=None, na_values='\\N')
airports.columns = ["ID", "NAME", "CITY", "COUNTRY", "IATA", "ICAO", "LATITUDE", "LONGITUDE", "ALTITUDE", "TIMEZONE",
                    "DST", "TZ", "TYPE", "SOURCE"]

# Read in the airlines data.
airlines = pd.read_csv("data/airlines.dat", header=None, na_values='\\N')
airlines.columns = ["ID", "NAME", "ALIAS", "IATA", "ICAO", "CALLSIGN", "COUNTRY", "ACTIVE"]

# Read in the routes data.
routes = pd.read_csv("data/routes.dat", header=None, na_values='\\N')
routes.columns = ["AIRLINE", "AIRLINE_ID", "SOURCE", "SOURCE_ID", "DEST", "DEST_ID", "CODESHARE", "STOPS", "EQUIPMENT"]
# routes = routes[(routes['SOURCE'] == "LEX")|(routes['SOURCE'] == "ORD")]

# Read in the planes data.
planes = pd.read_csv("data/planes.dat", header=None, na_values='\\N')
planes.columns = ["NAME", "IATA", "ICAO"]

# Read in the countries data.
countries = pd.read_csv("data/countries.dat", header=None, na_values='\\N')
countries.columns = ["NAME", "ISO", "DAFIF"]

setConnections = set()
dNodes = []


def get_cityIATAname(city_name):
    df = airports[airports["CITY"].str.casefold() == str(city_name).casefold()]
    if len(df) > 0:
        nameIATA = airports[airports["CITY"].str.casefold() == str(city_name).casefold()]["IATA"]
    return nameIATA.item()


def get_direct_connection(flyFromCity_IATA, flyToCity_IATA):
    df = routes[(routes['SOURCE'] == flyFromCity_IATA) & (routes['DEST'] == flyToCity_IATA)]
    transfer = 0
    bTransfer = False
    if df.empty:
        bTransfer = False
    else:
        bTransfer = True
    return bTransfer


def get_connection(start, goal):
    global dNodes, setConnections
    setConnections.add(str(start))
    strConnection = ""
    df = routes[(routes['SOURCE'] == start)]
    connections = df["DEST"].unique()
    connections.sort()
    output = 0
    for connection in connections:
        if connection is not None:
            if not connection in setConnections:
                setConnections.add(connection)
                bTransfer = get_direct_connection(connection, goal)
                if not bTransfer:
                    dNodes.append(connection)
                    get_connection(connection, goal)
                else:
                    dNodes.append(connection)
                    dNodes.append(goal)
                    break


def main():
    flyFromCity = "Lexington KY"
    flyToCity = "Mumbai"
    noTransfers = 2


    # # Describe the situation: from --> to city, number of transfers acceptable
    # global dNodes, setConnections
    # flyFromCity = "Lexington KY"
    # flyToCity = "Mumbai"
    # noTransfers = 2
    # strConnection = ""
    # # get IATA code for the respective cities
    # flyFromCity_IATA = get_cityIATAname(flyFromCity)
    # flyToCity_IATA = get_cityIATAname(flyToCity)
    # # transfers = get_direct_connection(flyFromCity_IATA, flyToCity_IATA,noTransfers)
    # bTransfer = get_direct_connection(flyFromCity_IATA, flyToCity_IATA)
    # if not bTransfer:
    #     if not str(flyFromCity_IATA) in setConnections:
    #         setConnections.add(flyFromCity_IATA)
    #         dNodes.append(flyFromCity_IATA)
    #         get_connection(flyFromCity_IATA, flyToCity_IATA)
    # else:
    #     if not str(flyFromCity_IATA) in setConnections:
    #         dNodes.append(flyFromCity_IATA)
    #         dNodes.append(flyToCity_IATA)
    #
    # # map out possibility of reaching destination from the source
    # if len(dNodes) <= (noTransfers + 2):
    #     for item in dNodes:
    #         strConnection = str(item) + "--> "
    #     print("You can fly via " + strConnection)
    # else:
    #     print("Connections could not be established with " + str(noTransfers) + " of transfers")
    #
    # # i = 0
    # # # if dfDirect.empty:
    # # if transfers < 0:
    # #     transfers=1
    # #     dNodes.add(flyFromCity)
    # #     i = get_connection(flyFromCity_IATA, flyToCity_IATA,transfers,noTransfers)
    # #     if i <= noTransfers:
    # #         print(flyFromCity + "-->")
    # # else:
    # #     dNodes.add(str(flyFromCity_IATA), str(flyToCity_IATA))
    # #     print(str(flyFromCity_IATA) + "-->" + str(flyToCity_IATA))


if __name__ == "__main__":
    main()
