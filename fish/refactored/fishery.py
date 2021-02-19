import notifiers
import clients
import factories
import formatters
import fish

# This is where your application logic is (application logic != business logic)
# This is at the very edge of your application
# You've imported all the tools you will need

# get the fish_species class instance
fish_species = factories.fish_factory(fish.FishSpecies)

# switch these around to toggle between remote and local data
#  fish_genera = factories.fish_factory(FishGenera)
fish_genera = factories.fish_factory(fish.FishGenera, client=clients.FishClientFile())

# Iterate the genera and report to the user interface via web sockets
for data in fish_genera:
    notifiers.FishUINotifier().notify(
        formatters.get_formatted_fish(data, lambda f: f"This is the genus name: {f}")
    )

# Iterate the species and report to the user interface via web sockets
for data in fish_species:
    notifiers.FishUINotifier().notify(
        formatters.get_formatted_fish(data, lambda f: f"This is the species name: {f}")
    )
